#import necessary libraries

from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
#Initialize ScrapingEssentials
new_urls = []

#Getting all the phones for Samsung

#This is the samsung specific

#We must start with an innoculous google search so that Amazon doesn't shut us down for being a crawler

#First, find the amazon seller's page on google

driver.get("https://www.google.com/search?q=samsung+on+amazon")
soup = BeautifulSoup(driver.page_source, "lxml")

samsunglink = ""
for med in soup.find_all("div", {"class":"med", "id": "res", "role": "main"}):
    samsungLink = med.find("a").get("href")
print(samsungLink)


