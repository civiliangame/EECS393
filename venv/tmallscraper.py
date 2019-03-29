from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import xlwt
import time
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



driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://samsung.tmall.com/")
time.sleep(3)
soup = BeautifulSoup(driver.page_source, "lxml")

samsungphones = soup.find("a", {"class": "jdbmc abs mcblack"})
#print(samsungphones.get("href"))
driver.get(samsungphones.get("href"))

time.sleep(.5)
soup = BeautifulSoup(driver.page_source, "lxml")


phonelist = []
for item in soup.find_all("a", {"class": "item-name"}):
    phonename = ""
    phoneprice = 0
    #print(item)
    phonename = item.get_text()
    pricediv = item.find_next_sibling("div")
    phoneprice = pricediv.get_text()
    phonelist.append([phonename, phoneprice])
print(phonelist)
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
