Python code to scrape data or access the APIs from store finders for some UK store chains:

* 🛒 [ALDI](https://www.aldi.co.uk/)
* 🥐 [GAIL's Bakery](https://gailsbread.co.uk/)
* 🍷 [Majestic Wine](https://www.majestic.co.uk/)
* 🛒 [Marks & Spencer](https://www.marksandspencer.com/)
* 🛒 [Morrisons](https://www.morrisons.com/)
* 🛒 [Sainsbury's](https://www.sainsburys.co.uk/)
* 🛒 [Tesco](https://www.tesco.com/)
* 🛒 [Waitrose](https://www.waitrose.com/)

Started as a joke to visualise the "posh areas of London" according to [this Reddit post](https://www.reddit.com/r/london/comments/wuwc6c/indicators_of_posh_area_in_london/).

All scrapers output GeoJSON with just the points and a store name for now. Other metadata (e.g. address/link to store page) is may be added later.

# Caveats

* There is no filtering or post-processing of data, and some of the data might be wrong (e.g. the coordinates for a Morrisons store are in the North Sea, but the same is shown in their official store finder 🤷🏻‍♂️)
* Some chains have stores outside the UK - where this data is automatically returned by the same store finder, it's included in the respective files.

Feel free to suggest other chains to scrape by raising an issue, or to make improvements by raising a PR.
