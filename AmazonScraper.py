#import necessary libraries

from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import xlwt
import time


def find_product_details(link, driver):
    driver.get(link)
    time.sleep(2)

    product_name = ""
    product_price = 0
    soup = BeautifulSoup(driver.page_source, "lxml")

    productTitle = soup.find("span", {"id": "productTitle"})

    try:
        product_name = productTitle.string.replace('\n', '').replace('  ', '')
        print(product_name)
        product_price = soup.find("span", {"id": "priceblock_ourprice"}).string
        print(product_price)

    except Exception:
        return []
    print ([product_name, product_price])
    return [product_name, product_price]



#
# from bs4 import BeautifulSoup
# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
# import xlwt
# import time
#
driver = webdriver.Chrome(ChromeDriverManager().install())
# Initiating the excel file
#Now we do the same for Apple
# driver.get("https://www.google.com/search?q=apple+on+amazon")
# soup = BeautifulSoup(driver.page_source, "lxml")
#
# appleLink = ""
# for med in soup.find_all("div", {"class":"med", "id": "res", "role": "main"}):
#     #print(med)
#     appleLink = med.find("a").get("href")
#     #print(appleLink)
#
#
# #We are now going to the amazon page
# li_list = []
# driver.get(appleLink)
# soup = BeautifulSoup(driver.page_source, "lxml")
# for header in soup.find_all("div", {"id": "header", "class": "a-row stores-row stores-widget-cf"}):
#     for li in header.find_all("li"):
#         #print(li)
#         for a in li.find_all("a"):
#             li_list.append(a.get("href"))
#
#
#
# theMobileLink = "https://www.amazon.com" + li_list[1]
#
# print(theMobileLink)
#
# #Go to the mobile link
# driver.get(theMobileLink)
#
# #now we want to narrow it down to smartphones
# time.sleep(3)
# soup = BeautifulSoup(driver.page_source, "lxml")
#
#
#
# #Find the individual listings for all the phones
# phoneLinks = []
#
# for storesRow in soup.find_all("div", {"class":"a-row stores-row stores-widget-atf"}):
#     for a in storesRow.find_all("a"):
#         temp = ("https://www.amazon.com"+a.get("href"))
#         if temp not in phoneLinks:
#             phoneLinks.append(temp)
#
# for link in phoneLinks:
#     find_product_details(link, driver)
#
# driver = webdriver.Chrome(ChromeDriverManager().install())
# # Initiating the excel file
# book = xlwt.Workbook(encoding="utf-8")
# sheet1 = book.add_sheet("Sheet 1")
#
#
# # Adding the correct columns
# sheet1.write(0, 0, "Phone Name")
# sheet1.write(0, 1, "Amazon Price")
# sheet1.write(0, 2, "Alibaba Price")
#
# book.save("result.xls")
#Getting all the phones for Samsung

#This is the samsung specific

#We must start with an innoculous google search so that Amazon doesn't shut us down for being a crawler

#First, find the amazon seller's page on google

driver.get("https://www.google.com/search?q=samsung+on+amazon")
soup = BeautifulSoup(driver.page_source, "lxml")

samsungLink = ""
for med in soup.find_all("div", {"class":"med", "id": "res", "role": "main"}):
    samsungLink = med.find("a").get("href")
#print(samsungLink)
driver.get(samsungLink)

#We are now going to the amazon page
# li_list = []
# driver.get(samsungLink)
# soup = BeautifulSoup(driver.page_source, "lxml")
# for header in soup.find_all("div", {"id": "header", "class": "a-row stores-row stores-widget-cf"}):
#     for li in soup.find_all("li"):
#         for a in li.find_all("a"):
#             if(a.get_text() == "SMARTPHONES"):
#                 smartphoneLink = a.get("href")
#                 print(smartphoneLink)
#
# #
# # mobileLinks = []
# # for a in li_list[1].find_all("a"):
# #     mobileLinks.append(a.get("href"))
#
# theMobileLink = "https://www.amazon.com" + smartphoneLink
# #print(theMobileLink)
#
# #Go to the mobile link
# driver.get(theMobileLink)
#
# #now we want to narrow it down to smartphones
# soup = BeautifulSoup(driver.page_source, "lxml")
# smartphones = soup.find("span", text="SMARTPHONES")
# smartphoneslink = smartphones.find_parent().get("href")
# smartphoneslink = "https://www.amazon.com" + smartphoneLink

#Get the page source.
soup = BeautifulSoup(driver.page_source, "lxml")

#initialize the list
li_list = []

#Each company calls their phones something different. This will account for it.
phoneNames = ["V Series", "G Series", "K Series", "W7", "SMARTPHONES", "IPHONE"]

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
                if(smartphoneLink not in phoneUrls):
                    phoneUrls.append(smartphoneLink)

#Now that we have a list of urls to hit, we are done.
#Usually, this will be only one, but LG will have 3.
#Since we want this to be as generic as possible for good programming practices, we will return a list.
print(phoneUrls)

driver.get("https://www.amazon.com"+ phoneUrls[0])
#driver.get(smartphoneslink)
time.sleep(3)
soup = BeautifulSoup(driver.page_source, "lxml")


#Find all the individual links for smartphones
phoneLinks = set([])

for storesRow in soup.find_all("div", {"class":"a-row stores-row stores-widget-atf"}):
    for a in storesRow.find_all("a"):
        phoneLinks.add("https://www.amazon.com"+a.get("href"))


for storesRow2 in soup.find_all("div", {"class":"a-row stores-row stores-widget-btf"}):
    #print(storesRow2)
    for div in storesRow2.find_all("div"):
        #print(div)
        for a in div.find_all("a"):
            potential = a.get("href")
            #if "Samsung" in potential and potential[0] == "/" and "comhttps:" not in potential:
            if "comhttps:" not in potential:
                phoneLinks.add("https://www.amazon.com"+potential)


print(phoneLinks)
for link in phoneLinks:
    find_product_details(link, driver)







