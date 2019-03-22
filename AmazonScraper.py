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




from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import xlwt
import time

driver = webdriver.Chrome(ChromeDriverManager().install())
# Initiating the excel file
#Now we do the same for Apple
driver.get("https://www.google.com/search?q=apple+on+amazon")
soup = BeautifulSoup(driver.page_source, "lxml")

appleLink = ""
for med in soup.find_all("div", {"class":"med", "id": "res", "role": "main"}):
    #print(med)
    appleLink = med.find("a").get("href")
    #print(appleLink)


#We are now going to the amazon page
li_list = []
driver.get(appleLink)
soup = BeautifulSoup(driver.page_source, "lxml")
for header in soup.find_all("div", {"id": "header", "class": "a-row stores-row stores-widget-cf"}):
    for li in header.find_all("li"):
        #print(li)
        for a in li.find_all("a"):
            li_list.append(a.get("href"))



theMobileLink = "https://www.amazon.com" + li_list[1]

print(theMobileLink)

#Go to the mobile link
driver.get(theMobileLink)

#now we want to narrow it down to smartphones
time.sleep(3)
soup = BeautifulSoup(driver.page_source, "lxml")



#Find the individual listings for all the phones
phoneLinks = []

for storesRow in soup.find_all("div", {"class":"a-row stores-row stores-widget-atf"}):
    for a in storesRow.find_all("a"):
        temp = ("https://www.amazon.com"+a.get("href"))
        if temp not in phoneLinks:
            phoneLinks.append(temp)

for link in phoneLinks:
    find_product_details(link, driver)

driver = webdriver.Chrome(ChromeDriverManager().install())
# Initiating the excel file
book = xlwt.Workbook(encoding="utf-8")
sheet1 = book.add_sheet("Sheet 1")


# Adding the correct columns
sheet1.write(0, 0, "Phone Name")
sheet1.write(0, 1, "Amazon Price")
sheet1.write(0, 2, "Alibaba Price")

book.save("result.xls")
#Getting all the phones for Samsung

#This is the samsung specific

#We must start with an innoculous google search so that Amazon doesn't shut us down for being a crawler

#First, find the amazon seller's page on google

driver.get("https://www.google.com/search?q=samsung+on+amazon")
soup = BeautifulSoup(driver.page_source, "lxml")

samsunglink = ""
for med in soup.find_all("div", {"class":"med", "id": "res", "role": "main"}):
    samsungLink = med.find("a").get("href")
#print(samsungLink)


#We are now going to the amazon page
li_list = []
driver.get(samsungLink)
soup = BeautifulSoup(driver.page_source, "lxml")
for header in soup.find_all("div", {"id": "header", "class": "a-row stores-row stores-widget-cf"}):
    for li in soup.find_all("li"):
        li_list.append(li)

mobileLinks = []
for a in li_list[1].find_all("a"):
    mobileLinks.append(a.get("href"))

theMobileLink = "https://www.amazon.com" + mobileLinks[1]
#print(theMobileLink)

#Go to the mobile link
driver.get(theMobileLink)

#now we want to narrow it down to smartphones
soup = BeautifulSoup(driver.page_source, "lxml")
smartphones = soup.find("span", text="SMARTPHONES")
smartphoneslink = smartphones.find_parent().get("href")
smartphoneslink = "https://www.amazon.com" + smartphoneslink

driver.get(smartphoneslink)
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
            if "Samsung" in potential and potential[0] == "/" and "twitter" "pinterest" "facebook" not in potential:
                phoneLinks.add("https://www.amazon.com"+potential)


print(phoneLinks)
for link in phoneLinks:
    find_product_details(link, driver)







