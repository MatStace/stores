import requests
import geojson
import json

r = requests.get("https://uberall.com//api/storefinders/JOWxbXjWIu1zWqNZM8k56PggggAdY6/locations/all?v=20211005&language=en&fieldMask=id&fieldMask=identifier&fieldMask=googlePlaceId&fieldMask=lat&fieldMask=lng&fieldMask=name&fieldMask=country&fieldMask=city&fieldMask=province&fieldMask=streetAndNumber&fieldMask=zip&fieldMask=businessId&fieldMask=addressExtra&")
stores = json.loads(r.text)['response']['locations']

print(f'Found {len(stores)} stores')

features = []

for store in stores:
    store_point = geojson.Point((float(store['lng']), float(store['lat'])))
    features.append(geojson.Feature(geometry=store_point))

all_stores = geojson.FeatureCollection(features)
with open('pret.json', 'w') as outfile:
    geojson.dump(all_stores, outfile, indent=2)
