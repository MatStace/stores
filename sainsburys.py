import requests
import geojson
import json
from progress.bar import Bar

base_url = 'https://stores.sainsburys.co.uk/api/v1/stores/?fields=slfe-list-2.21&api_client_id=slfe&lat=51.499568&lon=-0.101016&limit=50&store_type=main,local&sort=by_distance&within=1000&page={page}'
current_page = 1
features = []

bar = Bar('Downloading stores')

while True:
    r = requests.get(base_url.format(page = current_page))
    response = json.loads(r.text)

    if current_page == 1:
        bar.max = response['page_meta']['total']

    if len(response['results']) == 0:
        bar.finish()
        break

    for store in response['results']:
        store_point = geojson.Point((float(store['location']['lon']), float(store['location']['lat'])))
        features.append(geojson.Feature(geometry=store_point, properties={"name": store["other_name"]}))

    bar.index = len(features)
    bar.update()
    current_page += 1


all_stores = geojson.FeatureCollection(features)
with open('sainsburys.json', 'w') as outfile:
    geojson.dump(all_stores, outfile, indent=2)
