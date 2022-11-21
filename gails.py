import requests
import re
import geojson
from bs4 import BeautifulSoup

r = requests.get('https://gailsbread.co.uk/wpsl_stores-sitemap.xml')

soup = BeautifulSoup(r.text, features='xml')

stores = soup.select('url>loc')

print(f'Found {len(stores)} stores')

features = []

for store in stores:
    store_link = store.string
    if store_link != '':
        print(f'Processing store {store_link}')
        try:
            r = requests.get(store_link)
        except Exception as e:
            print(e)
            continue

        if r.status_code != 200:
            continue
        soup = BeautifulSoup(r.text, 'html.parser')
        map_js= soup.select('#wpsl-js-js-extra')[0].string

        lat = re.search('\"lat\":\"([0-9\-.]+)\"', map_js).group(1)
        long = re.search('\"lng\":\"([0-9\-.]+)\"', map_js).group(1)

        store_name = soup.select('title')[0].string.replace("| GAIL's Bakery","").strip()

        store_point = geojson.Point((float(long), float(lat)))
        features.append(geojson.Feature(geometry=store_point, properties={"name": store_name}))

all_stores = geojson.FeatureCollection(features)
with open('gails.json', 'w') as outfile:
    geojson.dump(all_stores, outfile, indent=2)
