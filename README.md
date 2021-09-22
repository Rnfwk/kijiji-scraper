# kijiji-scraper
A super easy-to-use, straightforward web scraper made with Python's Beautiful Soup to retreive specifically real-estate rental ads information from Kijiji.ca.

**Program workflow:**

1. Access the url you want to scrape
2. Loop through all result pages and get the url to each ad (rental listings) on each result page
3. Save the urls into a csv file
4. Acess each url saved in the file
5. Scrape the info of each ad
6. Save the ad details into a csv file

**How to use:**

Inside scraper.py, call the function **scrapeAd()** with 3 parameters, i.e. scrapeAd(urlCsvName, adCsvName, urlToScrape)

- urlCsvName: your desired name for the csv file for saving ad urls
- adCsvName: your desired name for the csv file for saving ad details
- urlToScrape: the starting url on kijiji.ca that you want to scrape

Example:

scrapeAd("long-term-rental-urls", "long-term-rental-ads", "https://www.kijiji.ca/b-apartments-condos/vancouver/c37l1700287")

**Notes:**

- Since the UI for long-term and short-term rental ads are not the same, the program will first determine the ad is which and proceed to locate relevant info
- After several testing, I concluded that the website will block requests after around 40 url requests at intervals, and hence the scraper would not able to scrape  all the ad urls. I put the program to sleep for 90 sec for every 40 ads scraped, this way all urls can be accessed and hence the ad info as well.
- Ad info not available or ads being removed will have their cell / row empty.

**Ad info being sraped:**

  "scraped_on",
  "posted_on",
  "title",
  "type",
  "short_term_rental",
  "price",
  "address",
  "size",
  "bedrooms",
  "bathrooms",
  "utilities",
  "wifi",
  "parking",
  "agreementType",
  "moveInDate",
  "petFriendly",
  "furnished",
  "appliances",
  "airCon",
  "outdoorSpace",
  "smoking",
  "amenities",
  "images",
  "description",
  "url"
