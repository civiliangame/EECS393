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
    #driver = webdriver.Chrome(ChromeDriverManager().install())
    r = requests.get("https://huawei.tmall.com/")
    #driver.get("https://huawei.tmall.com/")
    time.sleep(.5)
    soup = BeautifulSoup(r.content, "lxml")
    print(soup.prettify())

    print("HELLO BITCHES")
    print("")
    mandarinphone = soup.find("a", string ="手机专区", target="_blank")

    #print(phonelink)
    phonelink = mandarinphone.find_parent()
    print("phonelink is: "+ phonelink)

    siblings = phonelink.find_siblings()
    print("siblings are" + siblings)
    flagshiplist = []

    for link in phonelink.find_all("a"):
        flagshiplist.append(link.get("href"))
    print(flagshiplist)




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

huaweiScraper()








# username = "eecs293philliphwang"
# password = "philliphwang1"
#
# #time.sleep(5)
# login_iframe = driver.find_element_by_id("J_loginIframe")
# print("switched frames")
# driver.switch_to.frame(login_iframe)
# soup = BeautifulSoup(driver.page_source, "lxml")
# print(soup.prettify())
#
#
# if driver.find_element_by_id('J_Quick2Static').is_displayed():
#     driver.find_element_by_id('J_Quick2Static').click()
#     print("clicked")
# time.sleep(2)
# slipper = driver.find_element_by_css_selector('.nc-lang-cnt')
# h_position = slipper.location
# action = ActionChains(driver)
# action.drag_and_drop_by_offset(slipper, h_position['x'] + 300, h_position['y']).perform()
# time.sleep(3)
#
# driver.find_element_by_id("TPL_username_1").send_keys(username)
# driver.find_element_by_id("TPL_password_1").send_keys(password)
# driver.find_element_by_id("TPL_password_1").send_keys('keys.ENTER')
# soup = BeautifulSoup(driver.page_source, "lxml")
# print(soup.prettify())
# #usernameField = soup.find("input", {"class" : "field username-field"})
# #print(usernameField)
#
# # xpath = xpath_soup(usernameField)
# # print(xpath)
# # driver.find_element_by_xpath(xpath).send_keys(username)
#
