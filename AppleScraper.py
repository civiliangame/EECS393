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


phoneLinks = set([])

for storesRow in soup.find_all("div", {"class":"a-row stores-row stores-widget-atf"}):
    for a in storesRow.find_all("a"):
        print(a.get("href"))
        phoneLinks.add("https://www.amazon.com"+a.get("href"))