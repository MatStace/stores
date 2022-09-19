import requests
import geojson
from bs4 import BeautifulSoup

r = requests.get('https://www.waitrose.com/content/waitrose/en/bf_home/bf.html')

soup = BeautifulSoup(r.text, 'html.parser')

stores = soup.select('#global-form-select-branch option')

print(f'Found {len(stores)} stores')

features = []

for store in stores:
    store_id = store.get('value', None)
    store_name = store.string
    if store_id != '':
        print(f'Processing store {store_id} {store_name}')
        r = requests.get(f'https://www.waitrose.com/content/waitrose/en/bf_home/bf/{store_id}.html')
        if r.status_code != 200:
            continue
        soup = BeautifulSoup(r.text, 'html.parser')
        map_link = soup.select('a.load-branch-map')[0]
        store_point = geojson.Point((float(map_link.get('data-long')), float(map_link.get('data-lat'))))
        features.append(geojson.Feature(geometry=store_point, properties={"name": store_name}))

all_stores = geojson.FeatureCollection(features)
with open('waitrose.json', 'w') as outfile:
    geojson.dump(all_stores, outfile, indent=2)
