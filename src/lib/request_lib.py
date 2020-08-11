import os
import json
import requests
import pandas as pd
from PIL import Image
from io import BytesIO

# Example request: 'https://api.scryfall.com/cards/search?q=c%3Dwhite+cmc%3D1'
def query_scryfall(queryDict):
    site = "https://api.scryfall.com/cards/search?q="
    req = site + "+".join([str(k) + "%3D" + str(v) for k, v in queryDict.items()])
    r = requests.get(req)
    rJSON = r.json()
    if "data" in rJSON:
        return pd.DataFrame(rJSON['data'])
    else:
        print("Warning: Nothing found")
        return pd.DataFrame({k : [] for k in ['name', 'mana_cost', 'rarity', 'set', 'type_line']})


def query_google_imgs(rootDir, queryDict):
    pathKeys = os.path.join(rootDir, "src/keys.json")
    with open(pathKeys) as keyFile:
        keys = json.load(keyFile)

    site = "https://www.googleapis.com/customsearch/v1?"
    queryDictEff = {**keys, **queryDict, **{"alt" : "json"}}

    req = site + "&".join([str(k) + "=" + str(v) for k, v in queryDictEff.items()])
    r = requests.get(req)
    return r.json()


def get_image_by_url(url):
    return Image.open(BytesIO(requests.get(url).content))