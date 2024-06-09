"""
Created on Sun June 15 2024

@author: Erik
"""

import requests
import json
import pandas as pd

# variables #
cache_folder = 'C:/data_store/pokemon_name_cache.json'
pokemon_data_store = 'C:/data_store/pokemon_details.xlsx'

# functions for caching (pokeapi requests caching to be done)
def load_poke_cache(folder_location):
    try:
        # attempt to open cache file
        with open(folder_location, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        # if cache file does not exist, return empty dict
        return {}

def save_poke_cache(folder_location, cache_dictionary):
    # open file and save over with new contents
    with open(folder_location, 'w') as file:
        # save to file in JSON format
        json.dump(cache_dictionary, file)

# first iteration: get pokemon names and their types

## Extract (getting the data I want) ##

# # preload pokemon names (done only once or when checking for new pokemon names). KEEP AT 1 while developing to limit requests made
# preload_request = requests.get('https://pokeapi.co/api/v2/pokemon/?limit=1')
# # obtain results key and values
# preload_results = preload_request.json()['results']
# # dict to store cache
# preload_cache = {}
# # populate cache
# for result in preload_results:
#     name = result['name']
#     # check whether details have been obtained
#     details_obtained = False
#     # save to cache
#     preload_cache[name] = details_obtained
# # save preload cache
# save_poke_cache(cache_folder, preload_cache)

# load pokemon name cache
names_cache = load_poke_cache(cache_folder)

# initialise pokemon details dictionary
pokemon_details = {}

# iterate through cache
for pokemon_name in names_cache:
    # check cache, skip current iteration if value is True
    if names_cache[pokemon_name] == True:
        continue
    else:
        # get further details
        details = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}/")
        details = details.json()

        # save to details dict
        pokemon_details[pokemon_name] = {
            'name': details['name'],
            'pokemon_id': details['id'],
            'moves': details['moves'],
            'types': details['types'],
            'species': details['height'],
            'abilities': details['abilities'],
            'order': details['order'],
            'weight': details['weight'],
            'height': details['height']
        }
        
        # update cache to say pokemon details pulled
        # names_cache[pokemon_name] = False

        # save cache
        save_poke_cache(cache_folder, names_cache)

# Transform (altering datas format for purposes) ##
# convert dict to dataframe where keys (pokemon) become rows
df = pd.DataFrame.from_dict(pokemon_details, orient='index')

# Load (storing the prepared data for later analysis)
df.to_excel(pokemon_data_store, index=False)
