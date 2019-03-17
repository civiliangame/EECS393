from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import xlwt
import time


link = "https://www.amazon.com/dp/B07F88WT6B/ref=sspa_dk_detail_1?psc=1&pd_rd_i=B07F88WT6B&pd_rd_w=YfSX0&pf_rd_p=733540df-430d-45cd-9525-21bc15b0e6cc&pd_rd_wg=tE2Ye&pf_rd_r=98D0YGSB3KTJFVMKVK0M&pd_rd_r=c9ba7208-48f4-11e9-b0ce-1582fe71c4d3"
driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get(link)
time.sleep(2)

product_name = ""
product_price = 0
soup = BeautifulSoup(driver.page_source, "lxml")

productTitle = soup.find("span", {"id" : "productTitle"})

try:
    product_name = productTitle.string.replace('\n', '').replace('  ', '')
    print(product_name)
    product_price = soup.find("span", {"id": "priceblock_ourprice"}).string
    print(product_price)

except Exception:
    return []

return [product_name, product_price]