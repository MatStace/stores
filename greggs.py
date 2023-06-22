import requests
import geojson
import json

r = requests.get("https://production-digital.greggs.co.uk/api/v1.0/shops?latitude=54.006994430267156&longitude=-2.5038627362629144&distanceInMeters=500000")
stores = json.loads(r.text)

print(f'Found {len(stores)} stores')

features = []

for store in stores:
    store_point = geojson.Point((float(store['address']['longitude']), float(store['address']['latitude'])))
    features.append(geojson.Feature(geometry=store_point, properties={"name": store['shopName']}))

all_stores = geojson.FeatureCollection(features)
with open('greggs.json', 'w') as outfile:
    geojson.dump(all_stores, outfile, indent=2)
