#import necessary libraries

from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import xlwt
import time


#Will add element to list if it doesn't exist in it already.
def add_to_list(element, list):
    if element not in list:
        list.append(element)
    return list

#A method that will navigate to the offical company's page on amazon and return the link
#We want the offical seller's stuff because the official seller doens't have refurbished or used phones.
#Refurbished or used phones vary wildly in price, effectively making this app useless.
#After all, a highly damaged S9 might sell for $10, but the price of $10 is highly misleading.
#For our purposes, we will stick to only new phones by the offical seller. No shady stuff.
def navigate_to_amazon(companyName, driver):

    #We need to find the seller's page from google first for three reasons:
    #1. The seller's URL is, as far as I can tell, random characters and numbers.
    #This usually signifies that it's very volatile and subject to change on a whim.
    #If amazon changes how their sellers' url work, the code won't work and everything will crash.
    #2. It will look less suspicious from Amazon's bot-blocker if it shows that we came from a google search.
    #3. It looks cooler this way.
    driver.get("https://www.google.com/search?q=" + companyName + "+on+amazon")

    #Get the page source.
    soup = BeautifulSoup(driver.page_source, "lxml")

    #initialize variables.
    companyLink = ""

    #Find the first non-sponsored link. Sponsored links are generally bad and throw off everything.
    #This is why we are going to go through only the "main" class here.
    for med in soup.find_all("div", {"class": "med", "id": "res", "role": "main"}):
        #Find the href, or the url.
        companyLink = med.find("a").get("href")

    #Return it, and we now have the offical seller's page on amazon.
    print(companyLink)
    return companyLink


#A method that will go to the specific page where smartphones are being sold in that page.
#Big companies will have a bunch of products, but we are only interested in smartphones.
def find_smartphone_category(driver):

    #Get the page source.
    soup = BeautifulSoup(driver.page_source, "lxml")

    #initialize the list
    li_list = []

    #Each company calls their phones something different. This will account for it.
    phoneNames = ["V Series", "G Series", "K Series", "SMARTPHONES", "iPhone", "Smartphones"]

    #LG has a bunch of names for their phones, so we will make it return a list of urls for convenience.
    phoneUrls = []

    #All of our sellers (and most companies that sell more than one category of goods)
    #have convenient little tabs where they list their products. We will be using this to navigagte.

    #We are searching through all the "div" tags
    #that have "id" attribute "header" and "class" attribute "a-row stores-row stores-widget-cf"
    for header in soup.find_all("div", {"id": "header", "class": "a-row stores-row stores-widget-cf"}):

        #In HTML, there are generally two ways to make a list. unordered lists and ordered lists.
        #Amazon uses ordered lists, which have the tag of "li".
        #Thus, we will be finding all "li" tags
        for li in header.find_all("li"):

            #A generic tag that is used a lot is the "a" tag, which is usually the tag containing links and text.
            #This is usually the lowest in the html tree. We will be looking through all the a tags within the li tag.
            for a in li.find_all("a"):

                #If the text in the a tag has what a company would call their smartphones, we get that link.
                if (a.get_text() in phoneNames):
                    smartphoneLink = a.get("href")

                    #If that link isn't already appended, we append it.
                    phoneUrls = add_to_list("https://www.amazon.com"+ smartphoneLink, phoneUrls)

    #Now that we have a list of urls to hit, we are done.
    #Usually, this will be only one, but LG will have 3.
    #Since we want this to be as generic as possible for good programming practices, we will return a list.
    print(phoneUrls)
    return phoneUrls


#A method that will find all the links of whatever phones they have on their smartphone page.
def find_specific_phones(driver):

    #Download the page source for scraping
    soup = BeautifulSoup(driver.page_source, "lxml")

    phoneLinks = []

    #Amazon seller pages for smartphones have two different levels. the atf and the btf.
    #The atf is, generally speaking, the new and trending phone. This will show up top.
    #The btf is everything else. Since we want all phones, we will navigate through both.

    #For everything in the atf level
    for storesRow in soup.find_all("div", {"class": "a-row stores-row stores-widget-atf"}):
        for a in storesRow.find_all("a"):

            #Find every link there. This will almost always be a product link.
            potential = "https://www.amazon.com" + a.get("href")

            # We will add it to the list if it doesn't already exist in there and there is no funky business.
            # Sometimes it will accidentally capture weird links like "share to facebook"
            # These weird links are finished links, meaning that it will start with "https://"
            # while the good links start with "/" to show that it's a lower section of the tree.
            if "comhttps:" not in potential:
                add_to_list(potential, phoneLinks)

    #Now, we will do the same for the btf level. I didn't think it was worth making a new method for this
    #So please excuse the only copy and pasted code.
    for storesRow2 in soup.find_all("div", {"class": "a-row stores-row stores-widget-btf"}):
        for div in storesRow2.find_all("div"):
            for a in div.find_all("a"):
                potential = "https://www.amazon.com" + a.get("href")
                if "comhttps:" not in potential:
                    add_to_list(potential, phoneLinks)
    print(phoneLinks)
    return phoneLinks


#A method that, given the product link on any amazon page, will go and find the name and price and return it in a list
def find_product_details(link, driver):

    #Goes to the link
    driver.get(link)

    #Take a quick break to make sure that amazon doesn't block us for being bots
    #And, most importantly, to allow javascript to load in the page
    time.sleep(2)

    #Initializing fields
    product_name = ""
    product_price = 0

    #Get the page source
    soup = BeautifulSoup(driver.page_source, "lxml")


    #Find the product title
    productTitle = soup.find("span", {"id": "productTitle"})


    #Using trycatch because some sites don't have prices listed if it's out of stock
    #And that will crash the program.
    try:
        #The official name will have so much whitespace, which will look terrible on a spreadsheet.
        #We will remove it.
        product_name = productTitle.string.replace('\n', '').replace('  ', '')

        #Find the price
        product_price = soup.find("span", {"id": "priceblock_ourprice"}).string


    #If there is an exception, no problem. That means it's not in stock.
    #Carry on, carry on, as if nothing really matters.
    except Exception:
        return []

    #return the product name and product price in a list
    return [product_name, product_price]


#The main method
def main():
    #initialize company names that we will be scraping for
    company_names = ["lg", "samsung", "apple", "huawei"]

    products = []

    #This will give us a list of all the specific pages of all phones made by companies in our list.
    for company in company_names:
        #initialize selenium webdriver. This will be what we use to crawl amazon.
        driver = webdriver.Chrome(ChromeDriverManager().install())
        #Find the company's listing on amazon
        driver.get(navigate_to_amazon(company, driver))

        #Find where the company lists their smartphones.
        #For all companies except LG, this will just be a single site, with only LG having 3.
        companyphoneurls = find_smartphone_category(driver)
        for url in companyphoneurls:
            driver.get(url)
            time.sleep(1)

            products.append(find_specific_phones(driver))
        driver.close()


    driver = webdriver.Chrome(ChromeDriverManager().install())
    #Now that we have all the pages, we will go generate a spreadsheet for this stuff.


    output = []
    for company in products:
        for page in company:
            phoneinfo = find_product_details(page, driver)
            if len(phoneinfo) != 0:
                output.append(phoneinfo)
    print(output)


    for product in output:
        if len(product) == 0:
            output = output.remove(product)
    print(output)


    #Make a excel spreadsheet
    book = xlwt.Workbook(encoding="utf-8")
    sheet1 = book.add_sheet("Sheet 1")

    sheet1.write(0, 0, "Phone Name")
    sheet1.write(0, 1, "Amazon Price")
    sheet1.write(0, 2, "Alibaba Price")
    sheet1.write(0,3,"Company Name")

    print(len(output))
    for i in range(0, len(output)):
        for j in range(0, 2):
            print("i = " + str(i) + " , j = " + str(j))
            print(output[i][j])
            sheet1.write(i + 1, j, output[i][j])
    book.save("results.xls")

if __name__ == '__main__':
    main()