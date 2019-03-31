import os
import pickle
import json
import requests
import operator

def get_taboola_json(country_idx):
    if not os.path.exists("taboola"):
        os.makedirs("taboola")

    fname = "taboola/" + str(country_idx) + ".pkl"
    if os.path.exists(fname):
        with open(fname, 'rb') as f:
            json_data = pickle.load(f)
        return json_data

    url = "https://us-central1-vision-migration.cloudfunctions.net/la_hacks_2019?market_code="+str(country_idx)
    print("requesting ", url)
    req = requests.get(url)
    print("got request")
    json_data = json.loads(req.content.decode('utf-8'))

    with open(fname, 'wb') as f:
        pickle.dump(json_data, f)
    return json_data