from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import xlwt
import time

driver = webdriver.Chrome(ChromeDriverManager().install())
# Initiating the excel file
#Now we do the same for Apple
driver.get("https://www.google.com/search?q=LG+on+amazon")
soup = BeautifulSoup(driver.page_source, "lxml")

huaweiLink = ""
for med in soup.find_all("div", {"class":"med", "id": "res", "role": "main"}):
    #print(med)
    huaweiLink = med.find("a").get("href")
    #print(appleLink)


#We are now going to the amazon page
li_list = []
driver.get(huaweiLink)
soup = BeautifulSoup(driver.page_source, "lxml")
for header in soup.find_all("div", {"id": "header", "class": "a-row stores-row stores-widget-cf"}):

    for li in header.find_all("li"):
        #print(li)
        for a in li.find_all("a"):
            #li_list.append(a.get_text())
            li_list.append(a.get("href"))





print(li_list)

for i in range (len(li_list)):
    if li_list[i] == "V Series":
        print(str(i) + "   V series")
    if li_list[i] == "K Series":
        print(str(i) + "   K series")
theMobileLink = "https://www.amazon.com" + li_list[53]
theMobileLink2 = "https://www.amazon.com" + li_list[54]

print(theMobileLink)
print(theMobileLink2)

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

for storesRow in soup.find_all("div", {"class":"a-row stores-row stores-widget-btf"}):
    for a in storesRow.find_all("a"):

        temp = ("https://www.amazon.com"+a.get("href"))
        print(temp)
        if temp not in phoneLinks and "comhttps:" not in temp:
            phoneLinks.append(temp)

driver.get(theMobileLink2)

time.sleep(3)
soup = BeautifulSoup(driver.page_source, "lxml")


for storesRow in soup.find_all("div", {"class":"a-row stores-row stores-widget-atf"}):
    for a in storesRow.find_all("a"):
        temp = ("https://www.amazon.com"+a.get("href"))
        if temp not in phoneLinks:
            phoneLinks.append(temp)

for storesRow in soup.find_all("div", {"class":"a-row stores-row stores-widget-btf"}):
    for a in storesRow.find_all("a"):

        temp = ("https://www.amazon.com"+a.get("href"))
        print(temp)
        if temp not in phoneLinks and "comhttps:" not in temp:
            phoneLinks.append(temp)



print(phoneLinks)
