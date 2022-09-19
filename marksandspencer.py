import requests
import geojson
import json

r = requests.get('https://www.marksandspencer.com/webapp/wcs/stores/servlet/MSResStoreFinderConfigCmd?storeId=10151&langId=-24')

store_finder_config = json.loads(r.text.replace('STORE_FINDER_CONFIG=',''))

r = requests.get(f"{store_finder_config['storeFinderAPIBaseURL']}?apikey={store_finder_config['apiConsumerKey']}&latlong=51.50667191,-0.093357&limit=1000000&radius=100000")
stores = json.loads(r.text)['results']

print(f'Found {len(stores)} stores')

features = []

for store in stores:
    store_point = geojson.Point((float(store['coordinates']['longitude']), float(store['coordinates']['latitude'])))
    features.append(geojson.Feature(geometry=store_point, properties={"name": store['name']}))

all_stores = geojson.FeatureCollection(features)
with open('marksandspencer.json', 'w') as outfile:
    geojson.dump(all_stores, outfile, indent=2)
