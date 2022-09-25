import requests
import geojson
import json

# r = requests.get('https://my.morrisons.com/storefinder/scripts/main.js')
#
# store_finder_config = json.loads(r.text.replace('STORE_FINDER_CONFIG=',''))

r = requests.get("https://api.morrisons.com/location/v2//stores?apikey=kxBdM2chFwZjNvG2PwnSn3sj6C53dLEY&distance=5000000&lat=51&limit=1000&lon=0&offset=0&storeformat=supermarket")
stores = json.loads(r.text)['stores']

print(f'Found {len(stores)} stores')

features = []

for store in stores:
    store_point = geojson.Point((float(store['location']['longitude']), float(store['location']['latitude'])))
    features.append(geojson.Feature(geometry=store_point, properties={"name": store['storeName']}))

all_stores = geojson.FeatureCollection(features)
with open('morrisons.json', 'w') as outfile:
    geojson.dump(all_stores, outfile, indent=2)
