from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import re
import requests
import time


def scrapeAdUrl(urlCsvName, urlToScrape):
    urlCsv = open(urlCsvName + ".csv", "w")

    kijijiDomain = 'https://www.kijiji.ca'
    currentUrl = urlToScrape

    urlCount = 1
    while currentUrl:
        
        print("Accessing "  + currentUrl + "\n")

        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
        page_html = requests.get(currentUrl, headers = headers)
        pageParsed = soup(page_html.text, "lxml")

        # get the url of the ads
        containers = pageParsed.findAll("div", {"class":"search-item"})
        for container in containers:
            adPath = container['data-vip-url']
            urlCsv.write(kijijiDomain + adPath + "\n")

        # find the url of the next page
        nextUrl = pageParsed.find("a", {"title":"Next"})

        # check to see if there is a next page
        if nextUrl:
            currentUrl = kijijiDomain + nextUrl.get("href")

        else:
            print("You reached the end.\n")
            break

        urlCount += 1

    urlCsv.close()
    print(str(urlCount) + " urls scraped\n")

# you only need to call this function
def scrapeAd(urlCsvName, adCsvName, urlToScrape):
    
    scrapeAdUrl(urlCsvName, urlToScrape)

    adCsv = open(adCsvName+ ".csv", "w")
    headers = [
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
        "url",
        "\n"
        ]

    adCsv.write(",".join(headers))

    # read the ad urls scraped
    urlCsv = open(urlCsvName + ".csv", "r")
    adList = urlCsv.readlines()

    scrapeCount = 1

    for ad in adList:

        # sleep
        if scrapeCount % 40 == 0:
            time.sleep(90)  

        print('Scraping ad # ' + str(scrapeCount) + "\n" + ad.strip())

        # access the ad urls
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
        page_html = requests.get(ad.strip("\n"), headers = headers)
        pageParsed = soup(page_html.text, "lxml")

        # find elements (common for both rental types)
        findPostedOn = pageParsed.find("div", class_=re.compile("datePosted"))
        findTitle = pageParsed.find("h1", class_=re.compile("title"))
        findAddress = pageParsed.find("span", attrs={"itemprop": "address"})
        findDescription = pageParsed.find("div", class_=re.compile("descriptionContainer"))
        findShortRental = pageParsed.find(string="Short Term Rentals")
        images = pageParsed.findAll("img", class_=re.compile("image"))
        
        imageUrls = []
        for tag in images:
            imageUrls.append(tag.get("src"))
        imageUrlsString = " ".join(imageUrls)

        postedOn = findPostedOn.contents[1].get('title') if findPostedOn else ""
        title = findTitle.text.strip() if findTitle else ""
        address = findAddress.text.strip() if findAddress else ""
        description = findDescription.findChildren("div")[0].text.replace('\n', ' ') if findDescription else ""

        # for short-term rent type
        if findShortRental:
            findPrice = pageParsed.find(class_=re.compile("currentPrice"))
            findBedrooms = pageParsed.find("dt", string="Bedrooms")
            findBathrooms = pageParsed.find("dt", string="Bedrooms")
            findFurnished = pageParsed.find("dt", string="Furnished")
            findPetFriendly = pageParsed.find("dt", string="Pet Friendly")

            # assign respective values
            price = findPrice.contents[0].text if findPrice else ""
            bedrooms = findBedrooms.find_next("dd").text if findBedrooms else ""
            bathrooms = findBathrooms.find_next("dd").text if findBathrooms else ""
            furnished = findFurnished.find_next("dd").text if findFurnished else ""
            petFriendly = findPetFriendly.find_next("dd").text if findPetFriendly else ""

            # get current time
            localtime = time.localtime()
            scraped_on = time.strftime("%I:%M:%S %p", localtime)

            # write csv file
            adCsv.write(
                scraped_on + "," +
                postedOn.replace(",", " ") + "," +
                title.replace(",", " -") + "," + 
                "" + "," +
                "TRUE" + "," + 
                price.replace(",", "") + "," +  
                address.replace(",", " -") + "," +
                "" + "," +
                bedrooms.replace(",", " -") + "," +  
                bathrooms.replace(",", " -") + "," + 
                "" + "," +  
                "" + "," +  
                "" + "," + 
                "" + "," + 
                "" + "," + 
                petFriendly.replace(",", " -") + "," + 
                furnished.replace(",", " -") + "," + 
                "" + "," + 
                "" + "," +  
                "" + "," + 
                "" + "," + 
                "" + "," +
                imageUrlsString + "," +
                description.replace(",", " -").strip("\n") + "," + 
                ad) # do not need \n since 'ad' comes with it already
            
            print("Scraped" + "\n")
        
        # Long-term rental
        else:
            findType = pageParsed.find("span",class_=re.compile("noLabelValue"))
            findPrice = pageParsed.find(class_=re.compile("priceWrapper"))
            findBedrooms = pageParsed.find(class_=re.compile("noLabelValue"))
            findBathrooms = pageParsed.find(class_=re.compile("noLabelValue"))
            findUtilities = pageParsed.find("h4",text="Utilities Included") or pageParsed.find("dt",text="Utilities Included")
            findWifi = pageParsed.find("h4",text="Wi-Fi and More") or pageParsed.find("dt",text="Wi-Fi and More")
            findParking = pageParsed.find("h4",text="Parking Included") or pageParsed.find("dt",text="Parking Included")
            findAgreementType = pageParsed.find("h4",text="Agreement Type") or pageParsed.find("dt",text="Agreement Type")
            findMoveInDate = pageParsed.find("h4",text="Move-In Date") or pageParsed.find("dt",text="Move-In Date")
            findPetFriendly = pageParsed.find("h4",text="Pet Friendly") or pageParsed.find("dt",text="Pet Friendly")
            findSize = pageParsed.find("h4",text="Size (sqft)") or pageParsed.find("dt",text="Size (sqft)")
            findFurnished = pageParsed.find("h4",text="Furnished") or pageParsed.find("dt",text="Furnished")
            findAppliances = pageParsed.find("h4",text="Appliances") or pageParsed.find("dt",text="Appliances")
            findAirCon = pageParsed.find("h4",text="Air Conditioning") or pageParsed.find("dt",text="Air Conditioning")
            findOutdoorSpace = pageParsed.find("h4",text="Personal Outdoor Space") or pageParsed.find("dt",text="Personal Outdoor Space")
            findSmoking = pageParsed.find("h4",text="Smoking Permitted") or pageParsed.find("dt",text="Smoking Permitted")
            findAmenities = pageParsed.find("h4",text="Amenities") or pageParsed.find("dt",text="Amenities")

            # assign respective values
            type = findType.text if findType else ""
            price = findPrice.contents[0].text if findPrice else ""
            utilities = findUtilities.next_sibling.text if findUtilities else ""
            wifi = findWifi.next_sibling.text if findWifi else ""
            parking = findParking.next_sibling.text if findParking else ""
            agreementType = findAgreementType.next_sibling.text if findAgreementType else ""
            moveInDate = findMoveInDate.next_sibling.text if findMoveInDate else ""
            petFriendly = findPetFriendly.next_sibling.text if findPetFriendly else ""
            size = findSize.next_sibling.text if findSize else ""
            furnished = findFurnished.next_sibling.text if findFurnished else ""
            appliances = findAppliances.next_sibling.text if findAppliances else ""
            airCon = findAirCon.next_sibling.text if findAirCon else ""
            outdoorSpace = findOutdoorSpace.next_sibling.text if findOutdoorSpace else ""
            smoking = findSmoking.next_sibling.text if findSmoking else ""
            amenities = findAmenities.next_sibling.text if findAmenities else ""
            bedrooms = findBedrooms.find_next("span").text.replace('Bedrooms: ', '') if findBedrooms else ""
            bathrooms = findBathrooms.find_next("span").find_next("span").text.replace('Bathrooms: ', '') if findBathrooms else ""
            
            # get current time
            localtime = time.localtime()
            scraped_on = time.strftime("%I:%M:%S %p", localtime)

            # write csv file
            adCsv.write(
                scraped_on + "," +
                postedOn.replace(",", " ") + "," +
                title.replace(",", " -") + "," + 
                type.replace(",", " -") + "," +
                "FALSE" + "," + 
                price.replace(",", "") + "," +  
                address.replace(",", " -") + "," +
                size.replace(",", "") + "," +
                bedrooms.replace(",", " -") + "," +  
                bathrooms.replace(",", " -") + "," + 
                utilities.replace(",", " -") + "," +  
                wifi.replace(",", " -") + "," +  
                parking.replace(",", " -") + "," + 
                agreementType.replace(",", " -") + "," + 
                moveInDate.replace(",", " ") + "," + 
                petFriendly.replace(",", "") + "," + 
                furnished.replace(",", " -") + "," + 
                appliances.replace(",", " -") + "," + 
                airCon.replace(",", " -") + "," +  
                outdoorSpace.replace(",", " -") + "," + 
                smoking.replace(",", " -") + "," + 
                amenities.replace(",", " -") + "," +
                imageUrlsString + "," +
                description.replace(",", " -").strip("\n") + "," + 
                ad) # do not need \n since 'ad' comes with it already
            
            print("Scraped"+ "\n")

        scrapeCount += 1

    adCsv.close()
    print('All ads scraped!')


scrapeAd("long-term-urls", "long-term-ads", "https://www.kijiji.ca/b-apartments-condos/vancouver/c37l1700287")
