from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import xlwt
import time
import requests
from selenium.webdriver import ActionChains

#THIS METHOD IS NOT MY CODE. I FOUND IT ONLINE AND DECIDED TO INTEGRATE IT
#SINCE IT'S SUCH AN ESSENTIAL PART OF FINDING XPATH.
#MY GOD I JUST WISH I FOUND IT SOONER.
def xpath_soup(element):
    """
    Generate xpath from BeautifulSoup4 element
    :param element: BeautifulSoup4 element.
    :type element: bs4.element.Tag or bs4.element.NavigableString
    :return: xpath as string
    :rtype: str

    Usage:

    # >>> import bs4
    # >>> html = (
    # ...     '<html><head><title>title</title></head>'
    # ...     '<body><p>p <i>1</i></p><p>p <i>2</i></p></body></html>'
    # ...     )
    # >>> soup = bs4.BeautifulSoup(html, 'html.parser')
    # >>> xpath_soup(soup.html.body.p.i)
    '/html/body/p[1]/i'
    """
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:
        """
        @type parent: bs4.element.Tag
        """
        siblings = parent.find_all(child.name, recursive=False)
        components.append(
            child.name
            if siblings == [child] else
            '%s[%d]' % (child.name, 1 + siblings.index(child))
        )
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)

def close_login_screen(driver):
    try:
        soup = BeautifulSoup(driver.page_source, "lxml")
        closebutton = soup.find("div", {"class": "sufei-dialog-close", "id": "sufei-dialog-close"})
        print(closebutton)
        xpath = xpath_soup(closebutton)
        print(xpath)
        time.sleep(1)
        driver.find_element_by_id("sufei-dialog-close").click()
        driver.find_element_by_xpath(xpath_soup(closebutton)).click()
        driver.find_element_by_id("sufei-dialog-close").click()
        driver.find_element_by_id("sufei-dialog-close").click()
        driver.find_element_by_id("sufei-dialog-close").click()
        driver.find_element_by_id("sufei-dialog-close").click()
        driver.find_element_by_id("sufei-dialog-close").click()
        driver.find_element_by_id("sufei-dialog-close").click()

        #print("exited")
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, "lxml")
        print(soup.prettify())

    except Exception:
        print("no login required yet")
        pass
    return

#A method that gets rid of undesirable characters in a string.
#If a character in str is not in the string acceptables, it will take it out.
def purgeString(str, acceptables):
    length = len(str)
    index = 0
    newstr = str
    notdeadyet = True
    while notdeadyet == True:
        try:
            char = newstr[index]
        except Exception:
            notdeadyet = False
            break
        if newstr[index] not in acceptables:
            newstr = newstr.replace(newstr[index], "")
        else:
            index +=1
    return newstr

#A method that will get rid of everything after a period.
def purgeNum(num):
    index = len(num)
    for i in len(num):
        if num[i] == ".":
            index = i
    return num[0:index]

def huaweiScraper():

    #We can just use requests since they don't block it
    print("here we go")
    r = requests.get("https://huawei.tmall.com/")
    print("loaded")
    #driver.get("https://huawei.tmall.com/")
    time.sleep(.5)
    soup = BeautifulSoup(r.content, "lxml")
    #print(soup.prettify())

    print("HELLO BITCHES")
    print("")
    ft = soup.find("div", {"id": "ft"})
    #print(ft)

    ptlinks = []
    for outbox in soup.find_all("div", {"class": "outbox"}):

        if "navlist5" in str(outbox.find_parent()):
            #print(str(outbox.find_parent()))
            #print("outbox = " + str(outbox))
            for rel in outbox.find_all("div",{"class": "rel", "data-title" : "power by junezx 3.0"}):
                for a in rel.find_all("a", {"target": "_blank", "data-linkmode" : "ptlink"}):
                    #print("link is " + a.get("href"))
                    ptlinks.append("https:" + str(a.get("href")))
    return ptlinks
    #print(ptlinks)


    # for item in menus:
    #     candidate = item.find("a", string="手机专区")
    #     print(item)
    #     if candidate != None:
    #         phoneMenu = item
    #         break
    # print(phoneMenu)
    # siblings = phoneMenu.find_siblings()
    # print("siblings are" + str(siblings))
    # flagshiplist = []
    #
    # for link in phoneMenu.find_all("a"):
    #     flagshiplist.append(link.get("href"))
    # print(flagshiplist)




def samsungScraper():
    driver = webdriver.Chrome(ChromeDriverManager().install())

    # driver.get("https://detail.tmall.com/item.htm?spm=a1z10.4-b-s.w4007-18945924930.7.681155f7PVwKkP&id=579791278840&sku_properties=10004:709990523")
    # close_login_screen(driver)

    driver.get("https://samsung.tmall.com/")
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, "lxml")

    samsungphones = soup.find("a", {"class": "jdbmc abs mcblack"})
    #print(samsungphones.get("href"))
    driver.get(samsungphones.get("href"))

    time.sleep(.5)
    soup = BeautifulSoup(driver.page_source, "lxml")

    nonnumbers = "0123456789."
    nonchinese = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&\()*+,-./:;<=>?@[]^_`{|}~"
    phonelist = []
    phonename = ""
    phoneprice = 0

    for item in soup.find_all("a", {"class": "item-name"}):
        phonename = item.get_text().replace("Samsung/", "")
        pricediv = item.find_next_sibling("div")
        phoneprice = pricediv.get_text().replace('\n', '')
        phonename = purgeString(phonename, nonchinese)
        phoneprice = purgeString(phoneprice, nonnumbers)
        print(phonename)
        print(phoneprice)
        phonelist.append([phonename, phoneprice])
    print(phonelist)
    return phonelist


def samsungScraper2():
    #We can just use requests since they don't block it
    print("here we go")
    r = requests.get("https://samsung.tmall.com/")
    print("loaded")



    #driver.get("https://huawei.tmall.com/")
    time.sleep(.5)
    soup = BeautifulSoup(r.content, "lxml")

    samsungphones = soup.find("a", {"class": "jdbmc abs mcblack"})
    print(samsungphones.get("href"))
    r = requests.get("https:" + str(samsungphones.get("href")))

    time.sleep(.5)
    soup = BeautifulSoup(r.content, "lxml")

    nonnumbers = "0123456789."
    nonchinese = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&\()*+,-./:;<=>?@[]^_`{|}~"
    phonelist = []
    phonename = ""
    phoneprice = 0

    for item in soup.find_all("a", {"class": "item-name"}):
        phonename = item.get_text().replace("Samsung/", "")
        pricediv = item.find_next_sibling("div")
        phoneprice = pricediv.get_text().replace('\n', '')
        phonename = purgeString(phonename, nonchinese)
        phoneprice = purgeString(phoneprice, nonnumbers)
        print(phonename)
        print(phoneprice)
        phonelist.append([phonename, phoneprice])
    print(phonelist)
    return phonelist

def applescraper():
    print("here we go")
    r = requests.get("https://apple.tmall.com/")
    print("loaded")
    soup = BeautifulSoup(r.content, "lxml")
    iphones = soup.find("a", string="iPhone")
    print(iphones)
    iphones_link = "https:" + iphones.get("href")


    r = requests.get(iphones_link)
    soup = BeautifulSoup(r.content, "lxml")
    specific_iphones = []

    for phonelink in soup.find_all("a", string="购买"):
        url = str(phonelink.get("href"))
        print(url)
        specific_iphones.append(url)
    return specific_iphones

def specific_phones(link):
    r = requests.get(link)
    source_code = str(r.content)
    shopsetup = source_code.find("TShop.Setup")

    print("T shop starts from: " + str(shopsetup))
    source_code = source_code[shopsetup:]
    print("castrated")
    priceList = []

    notdeadyet = True
    while notdeadyet == True:

        priceIndex = source_code.find("\"price\":\"")

        if priceIndex == -1:
            notdeadyet = False
        else:
            source_code = source_code[priceIndex + 9:]
            periodIndex = source_code.find(".")
            priceList.append(int(source_code[:periodIndex]))
    #print(priceList)
    phoneprice = min(priceList)
    print(phoneprice)

    soup = BeautifulSoup(r.content, "lxml")
    meta = soup.find("meta", {"name": "keywords"})
    phonename = (meta.get("content"))
    return[phonename, phoneprice]
    #print(source_code)


def xiaomiscraper():
    print("here we go")
    r = requests.get("https://xiaomi.tmall.com/")
    print("loaded")
    soup = BeautifulSoup(r.content, "lxml")
    print(soup)
    topbanner = soup.find("div", {"class": "topbanner"})
    power = topbanner.find("div", {"class": "rel", "data-title" : "power by junezx 3.0"})
    div = power.find("div")
    phoneKey = ""
    urls = []
    for a in div.find_all("a"):
        if "565px" in a.get("style"):
            phoneKey = a.get("data-appid")
    for allDivs in soup.find_all("div"):
        lock = allDivs.get("data-widget-config")
        if lock == None:
            continue
        if phoneKey in lock:
            for a in allDivs.find_all("a"):
                detailedUrl = a.get("href")
                if detailedUrl != None:
                    urls.append("https:" + detailedUrl)


    for a in div.find_all("a"):
        if "639px" in a.get("style"):
            phoneKey = a.get("data-appid")
    for allDivs in soup.find_all("div"):
        lock = allDivs.get("data-widget-config")
        if lock == None:
            continue
        if phoneKey in lock:
            for a in allDivs.find_all("a"):
                detailedUrl = a.get("href")
                if detailedUrl != None:
                    urls.append("https:" + detailedUrl)
    print(urls)
    return urls




