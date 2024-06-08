# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 18:35:38 2024

@author: Erik
"""

# import
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import pandas as pd

# variables #

# page count to match pagination pattern in URL
page_count = 1

# list to store dict of book details
book_details = []

# location on pc to save the data
save_folder = 'C:/data_store'

# dict containing possible book ratings
ratings_dict = {'Zero': 0, 'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}

# start driver
driver = webdriver.Chrome()
driver.get('http://books.toscrape.com/index.html')

# extract information #
while True:
    
    # UMR parameterization
    url = f'http://books.toscrape.com/catalogue/page-{page_count}.html'

    # make request
    response = requests.get(url)
    
    # Specify the correct encoding (e.g., 'utf-8'). I.e., the 
    response.encoding = 'utf-8'
    
    # 200 indicates sucessful get request
    if response.status_code == 200:
        # save response as string
        page_html = response.text
        
        # parse data
        soup = BeautifulSoup(page_html, 'html.parser')
        
        # retrieve all article elements with class product_pod. This contains all the information desired
        book_sections = soup.find_all('article', class_='product_pod')
        
        # extract desired information from book_section
        for book_section in book_sections:
            
            # retrieve book name
            name_element = book_section.find('h3')
            name_element_text = name_element.get_text().strip()
            
            # retrieve book price
            price_element = book_section.find('p', class_='price_color')
            price_element_text = price_element.get_text().strip()
            
            # retrieve rating
            star_rating_element = book_section.select('p[class*="star-rating"]') # select by CSS selector using substring
            for key in ratings_dict.keys():
                # check if key in stringified star_rating_element
                if key in str(star_rating_element):
                    # if key present then using key to obtain value gets correct rating
                    star_rating_number = ratings_dict[key]
                    
            # retrieve in stock details
            stock_element = book_section.find('p', class_='instock availability')
            stock_element_text = stock_element.get_text().strip()
            
            # enter book link
            rel_link = book_section.find('h3').find('a')['href'] # returns relative link
            full_link = f'http://books.toscrape.com/catalogue/{rel_link}' # combine to get full link
            driver.get(full_link) # access link
            
            # parse subpage data
            current_page_html = driver.page_source # get page source
            
            # get genre
            page_links = BeautifulSoup(current_page_html, 'html.parser') # parse data
            page_links = page_links.find('ul', class_='breadcrumb').find_all('a')
            genre_text = page_links[2].get_text()
            
            # get book description
            product_page = BeautifulSoup(current_page_html, 'html.parser')            
            product_description = product_page.find('div', id='product_description') # neighbouring element has id
            if product_description == None:
                book_description_text = 'No description'
            else:
                book_description_text = product_description.find_next_sibling().get_text() # reference through neighbouring element
            
            driver.back() # go back to previous page
            
            # store as dict
            book_details_dict = {'Name': name_element_text, 
                                  'Genre': genre_text,
                                  'Price': price_element_text, 
                                  'Rating': star_rating_number,
                                  'In_Stock': stock_element_text,
                                  'Description': book_description_text
                                  }
            
            # append dict to list
            book_details.append(book_details_dict)
            
            
    else:
        print(f'Failed to retrieve webpage: {response.status_code}')
        break
    
    page_next_link = soup.find('li', class_='next')
    if page_next_link is None:
        break
        
    # update page counter
    print(f'page {page_count} scraped')
    page_count = page_count + 1

# close selenium
driver.quit()

# create dataframe from book_details if book_details contains info
if len(book_details) > 0:
    print(f'page {page_count} scraped')
    
    # create dataframe from list of dictionaries
    df_books = pd.DataFrame(book_details)
    
    # data processing
    df_books.rename(columns={'Price': 'Price (£)'}, inplace=True) # rename col
    df_books['Price (£)'] = df_books['Price (£)'].str.replace('£', '').astype(float) # convert to float
    
# create dataframe from book_details if book_details contains info
if len(book_details) > 0:
    print(f'page {page_count} scraped')
    
    # create dataframe from list of dictionaries
    df_books = pd.DataFrame(book_details)
    
    # data processing
    df_books.rename(columns={'Price': 'Price (£)'}, inplace=True) # rename col
    df_books['Price (£)'] = df_books['Price (£)'].str.replace('£', '').astype(float)
    
    # save folder
    df_books.to_excel(f"{save_folder}/to_scrape_books.xlsx", index=False)