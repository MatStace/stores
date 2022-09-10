import requests
import geojson
import json
from progress.bar import Bar

base_url = 'https://stores.aldi.co.uk/store-finder?q=51%2C0&r=1000&qp=My+Location&l=en&per=50&offset={offset}'
current_offset = 0
features = []

bar = Bar('Downloading stores')

while True:
    r = requests.get(base_url.format(offset = current_offset), headers = {'Accept': 'application/json'})
    response = r.json()

    if current_offset == 0:
        bar.max = response['response']['count']

    stores = response['response']['entities']

    if len(stores) == 0:
        bar.finish()
        break

    for store in stores:
        store_point = geojson.Point((float(store['profile']['yextDisplayCoordinate']['long']), float(store['profile']['yextDisplayCoordinate']['lat'])))
        features.append(geojson.Feature(geometry=store_point, properties={"name": store['profile']['c_metaTitle']}))

    bar.index = len(features)
    bar.update()
    current_offset = len(features)

all_stores = geojson.FeatureCollection(features)
with open('aldi.json', 'w') as outfile:
    geojson.dump(all_stores, outfile, indent=2)
