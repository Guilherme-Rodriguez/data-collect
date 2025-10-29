# %%

import requests

def get_pokemons(**kwargs):
    url = "https://pokeapi.co/api/v2/pokemon/"
    resp = requests.get(url)
    resp.json()
    return resp

# %%
resp = get_pokemons(limit = 5, offset = 15)
resp.json()

# %%
