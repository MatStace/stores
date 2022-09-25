import requests
import geojson
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from progress.bar import Bar

ua = UserAgent()

r = requests.get('https://www.tesco.com/store-locator/directory', headers = { 'User-Agent': ua.safari } )

soup = BeautifulSoup(r.text, 'html.parser')

regions = soup.select('.Directory-listLink')

print(f'Found {len(regions)} regions')

features = []
store_links = []

bar = Bar('Downloading regions', max=len(regions))

for region in regions:
    region_link = region['href']
    bar.suffix = '%(index)d/%(max)d ' + region_link

    if '/' in region_link:
        # regions with only 1 store redirect straight to the store
        store_links.append(region_link)
    else:
        r = requests.get(f'https://www.tesco.com/store-locator/{region_link}', headers = { 'User-Agent': ua.safari } )

        soup = BeautifulSoup(r.text, 'html.parser')

        stores = soup.select('.LocationList .Teaser-button')
        #print(f'Found {len(stores)} stores')

        for store in stores:
            store_links.append(store['href'])
    bar.next()

bar.finish()

print(f'Found {len(store_links)} stores total')

bar = Bar('Downloading stores', max=len(store_links))
for store_link in store_links:
    bar.suffix = '%(index)d/%(max)d ' + store_link
    r = requests.get(f'https://www.tesco.com/store-locator/{store_link}', headers = { 'User-Agent': ua.safari } )

    soup = BeautifulSoup(r.text, 'html.parser')

    longitude = soup.select('meta[itemprop="longitude"]')[0]
    latitude = soup.select('meta[itemprop="latitude"]')[0]

    store_point = geojson.Point((float(longitude.get('content')), float(latitude.get('content'))))

    features.append(geojson.Feature(geometry=store_point))
    bar.next()

bar.finish()

all_stores = geojson.FeatureCollection(features)
with open('tesco.json', 'w') as outfile:
    geojson.dump(all_stores, outfile, indent=2)
