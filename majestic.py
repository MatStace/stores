import requests
import geojson
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
ua = UserAgent()

r = requests.get('https://www.majestic.co.uk/stores', headers = { 'User-Agent': ua.random } )

soup = BeautifulSoup(r.text, 'html.parser')

regions = soup.select('.stores-container .Div .Div a')

print(f'Found {len(regions)} regions')

features = []

for region in regions:
    region_link = region['href']
    print(f'Processing region {region_link}')
    r = requests.get(f'https://www.majestic.co.uk{region_link}', headers = { 'User-Agent': ua.random } )

    soup = BeautifulSoup(r.text, 'html.parser')
    stores = soup.select('.view-on-map')

    print(f'Found {len(stores)} stores')

    for store in stores:
        try:
            store_point = geojson.Point((float(store.get('data-long')), float(store.get('data-lat'))))
        except:
            continue
        features.append(geojson.Feature(geometry=store_point))

all_stores = geojson.FeatureCollection(features)
with open('majestic.json', 'w') as outfile:
    geojson.dump(all_stores, outfile)
