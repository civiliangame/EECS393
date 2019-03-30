from bs4 import BeautifulSoup
import xlwt
import time
import requests
import threading
import timeout_decorator
#Global Variables
samsungList = []
appleList = []
huaweiList = []
xiaomiList = []
resultList = []



#A method that finds goes to a page and returns the source code.
#With China being halfway around the world and all, sometimes connection is difficult.
#Because of that, we will make it timeout in 10 seconds.
#If it didn't load in 10 seconds, we can just try again.
@timeout_decorator.timeout(10, use_signals=False)
def getPage(link):
    print("starting getPage")
    r = requests.get(link)
    time.sleep(.5)
    return r.content

#A wrapper class for getPage. If it gets a timeoutError, we want to make it start again until it does.
def neverSayDie(link):
    print("starting neverSayDie")
    done = False;
    while not done:
        try:
            content = getPage(link)
        except Exception as e:
            print(e)
            continue
        done = True
    print("loaded")
    return content

#A method that gets rid of undesirable characters in a string.
#If a character in str is not in the string acceptables, it will take it out.
def purgeString(str, acceptables):

    print("starting purgeString")
    #initializing variables
    index = 0
    newstr = str

    #Go through the string until we run out of characters
    while 1 == 1:

        #Trycatch since there will be an out of bounds error
        try:
            #See if it will go out of bounds
            char = newstr[index]

        #If it does, break. We got what we needed.
        except Exception:
            break

        #If the current character is not in the list of acceptable characters:
        if newstr[index] not in acceptables:
            #Replace it with a space, basically getting rid of it
            newstr = newstr.replace(newstr[index], "")

        #If it's good, increment the counter
        else:
            index +=1

    #Return the new clean string
    return newstr

#A method that will get rid of everything after a period.
def purgeNum(num):
    print("starting purgeNum")
    index = len(num)
    for i in len(num):
        if num[i] == ".":
            index = i
    return num[0:index]

#A method that will return all the phone name/price pairs for samsung phones
#It will return a list of lists.
def samsungScraper():
    print("starting samsungScraper")
    global samsungList
    print("here we go")

    #Go to the tmall listing with all the samsung products
    content = neverSayDie("https://samsung.tmall.com/")
    

    time.sleep(.5)
    soup = BeautifulSoup(content, "lxml")

    #Samsung phones are in the a tag with class attribute "jdbmc abs mcblack" for some reason.
    #I don't know why. Don't ask me. I'm just finding patterns and then using them.
    samsungphones = soup.find("a", {"class": "jdbmc abs mcblack"})

    #Go to the new page listing all the samsung phones that we just found.
    content = neverSayDie("https:" + str(samsungphones.get("href")))

    time.sleep(.5)
    soup = BeautifulSoup(content, "lxml")

    #We are defining what letters/numbers/symbols we want in the string.
    nonnumbers = "0123456789."
    nonchinese = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&\()*+,-./:;<=>?@[]^_`{|}~"
    phonelist = []

    #For all the phones listed in this new page:
    for item in soup.find_all("a", {"class": "item-name"}):

        #Clean up the data we're getting
        phonename = item.get_text().replace("Samsung/", "")
        pricediv = item.find_next_sibling("div")
        phoneprice = pricediv.get_text().replace('\n', '')
        phonename = purgeString(phonename, nonchinese)
        phoneprice = purgeString(phoneprice, nonnumbers)

        #Append a list of name/price to the phone list
        phonelist.append([phonename, phoneprice, "Samsung"])

    #Return the phonelist
    samsungList = phonelist

#A method that will go through the huawei site of tmall and find the links for the specific phones listed
def huaweiScraper():
    print("starting huaweiScraper")
    global huaweiList
    print("here we go")

    #Go to the site with the requests library.
    content = neverSayDie("https://huawei.tmall.com/")
    
    time.sleep(.5)

    #Download the content
    soup = BeautifulSoup(content, "lxml")

    #Initializing the list that we want to return
    ptlinks = []

    #It's going to get a lot hectic from here. If you want to follow along,
    #I suggest going through inspect element for the site and seeing what I'm doing

    #First, we look at all the div tags with class attribute outbox.
    for outbox in soup.find_all("div", {"class": "outbox"}):

        #navlist5 is basically the trigger. We want the 5th trigger for phones.
        if "navlist5" in str(outbox.find_parent()):

            #We are narrowing down the search to the stuff that comes up if you hover over the 5th trigger
            for rel in outbox.find_all("div",{"class": "rel", "data-title" : "power by junezx 3.0"}):
                #We want to find the urls
                for a in rel.find_all("a", {"target": "_blank", "data-linkmode" : "ptlink"}):
                    #Find all the tags with "href" append it to the list
                    ptlinks.append(["https:" + str(a.get("href")), "Huawei"])

    #We now have all the links that are listed for their phones. We can return it.
    huaweiList = ptlinks



#A method that scrapes the info for iphones of tmall
def applescraper():
    print("starting appleScraper")
    global appleList
    print("here we go")
    #Go to Apple's page for tmall
    content = neverSayDie("https://apple.tmall.com/")
    
    soup = BeautifulSoup(content, "lxml")

    #Find the category that says "iphone". How nice of them to use English for the first time.
    iphones = soup.find("a", string="iPhone")
    #Find the link for iphones.
    iphones_link = "https:" + iphones.get("href")

    #Go to that newly discovered link.
    content = neverSayDie(iphones_link)
    soup = BeautifulSoup(content, "lxml")

    #A list that will hold the links for specific iphones on sale there.
    specific_iphones = []

    #Apparently that chinese word there means "buy".
    #How nice of them to make it very simple to find the listings for individual iphones.
    for phonelink in soup.find_all("a", string="购买"):
        #Get the url from this page and add it to the list
        url = str(phonelink.get("href"))
        specific_iphones.append([url, "Apple"])
    appleList = specific_iphones

#A method that finds the urls of all phones listed on Xiaomi's tmall page.
#It was originally going to be LG phones, but Tmall doesn't have LG phones
#And amazon doesn't have xiaomi phones.
def xiaomiscraper():
    print("starting xiaomiscraper")
    global xiaomiList
    #Go to the link
    print("here we go")
    content = neverSayDie("https://xiaomi.tmall.com/")
    

    #Download the page source
    soup = BeautifulSoup(content, "lxml")

    #Start narrowing the search. We want to look in just the top banner first.
    topbanner = soup.find("div", {"class": "topbanner"})

    #Narrow it down further to the place where we want.
    power = topbanner.find("div", {"class": "rel", "data-title" : "power by junezx 3.0"})
    #It's going to be in the first div tag
    div = power.find("div")

    #We need to talk about keys.
    #The way this page is structured is as follows:
    #1. The banner is a giant image file. This means that there is literally no text inside this banner.
    #2. They divided the banner into little subsections based on location.
    #3. Each location generates a unique "key" for the website to follow. This seems to be randomly generated each time.
    #4. Each key will hold the data and url for that specific category listed on the banner in an image.
    #5. Each key is a "trigger", meaning that you'll be able to get the data only if you have the unique code that is the key.
    #6. In order to find the url for phones, we need to find the keys based on location of the banner and match it to the lock.
    phoneKey = ""
    urls = []

    #Find all the a tags in the div tag from earlier.
    for a in div.find_all("a"):
        #If the location is at 565 pixels
        if "565px" in a.get("style"):
            #We found our key.
            phoneKey = a.get("data-appid")

    #Now, we will find a lock that matches.
    #This can be done pretty carelessly since the key is unique.
    for allDivs in soup.find_all("div"):

        #Find potential locks
        lock = allDivs.get("data-widget-config")

        #if the lock doesn't exist, just carry on.
        if lock == None:
            continue

        #If the key matches the lock, we found our url.
        if phoneKey in lock:
            for a in allDivs.find_all("a"):
                detailedUrl = a.get("href")

                #Some locks have nothing of fruition behind it, so we will not consider that.
                if detailedUrl != None:

                    #Append it to the list.
                    urls.append(["https:" + detailedUrl, "Xiaomi"])

    #Same thing as above, since Xiaomi seems to have two cell phone categories.
    #The only difference is that the location has changed. Everything else is the same.
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
                    urls.append(["https:" + detailedUrl, "Xiaomi"])

    #Now that we have a list of all urls, we can just return it.
    xiaomiList = urls

#A method that takes a specific listing page as input and returns the name/price as output.
def specific_phones(link, company):
    print(link)
    global resultList
    print("starting specific_phones")
    content = neverSayDie(link)
    source_code = str(content)

    #This would have been difficult, but luckily I found out that they store all the pricing data in a little sheet
    #Located at the bottom of the page named "TShop.Setup".
    shopsetup = source_code.find("TShop.Setup")

    #We don't care about anything before the sheet for now, so get rid of it all.
    source_code = source_code[shopsetup:]

    #They have a lot of prices listed, so we're going to have to sort through them all.
    priceList = []

    #We are going to parse through this sheet as if it were a very, very, very long string.
    notdeadyet = True
    while notdeadyet == True:

        #They have prices listed as "price":"[price here]"
        #We are going to search for this specific string.
        priceIndex = source_code.find("\"price\":\"")

        #The find method will return -1 if it has no more matches. In that case, we can quit.
        if priceIndex == -1:
            notdeadyet = False

        #If there is a price listed:
        else:

            #We get rid of the beginning part of the string as it's not relevant.
            source_code = source_code[priceIndex + 9:]
            #We go until we hit the period, which signifies the end of the chinese yuen.
            periodIndex = source_code.find(".")

            #The string between the beginning of the source code and periodIndex is the price.
            #Turn that into an int and append it to the list.
            priceList.append(int(source_code[:periodIndex]))

    #We just want the minimum price, since everything else is just configuration.
    phoneprice = min(priceList)

    #Now, we want to see the source code to figure out what the name of this phone is.
    soup = BeautifulSoup(content, "lxml")
    #It's conveniently located in a tag named meta with attribute name = "keywords"
    meta = soup.find("meta", {"name": "keywords"})
    #Get the name
    phonename = (meta.get("content"))

    #We now have a nice pairing of phonename and phoneprice.
    resultList.append([phonename, phoneprice, company])

#Main Method
def main():

    #Defining Global Variables
    global appleList
    global huaweiList
    global xiaomiList
    global samsungList

    #Define Threads and start scraping apple, huawei,xiaomi, and samsung
    t1 = threading.Thread(target=applescraper)
    t2 = threading.Thread(target=huaweiScraper)
    t3 = threading.Thread(target=xiaomiscraper)
    t4 = threading.Thread(target=samsungScraper)

    #Start Threads
    t1.start()
    t2.start()
    t3.start()
    t4.start()

    #Join Threads
    t1.join()
    t2.join()
    t3.join()
    t4.join()


    #This is going to be where everything comes together for the first time
    bigList = []

    #Move everything to biglist
    for a in appleList:
        bigList.append(a)
    for h in huaweiList:
        bigList.append(h)
    for x in xiaomiList:
        bigList.append(x)

    #The list of threads
    jobs = []

    #Assign threads
    for i in range(0, len(bigList)):
        thread = threading.Thread(target=specific_phones, args=(bigList[i][0], bigList[i][1]))
        jobs.append(thread)

    #Start the jobs
    for j in jobs:
        j.start()
    #Join the jobs
    for j in jobs:
        j.join()

    #Samsung was nice and let us skip a step. Now we're going to add it back in.
    for samsungphone in samsungList:
        #Get rid of the period and the numbers after it for consistency
        samsungphone[1] = int(samsungphone[1][:samsungphone[1].find(".")])
        #Append it to the resultsList
        resultList.append(samsungphone)

    #This is the final list
    finalList = []

    #Migrate everything over and also add the source
    for result in resultList:
        finalList.append([result[0], "元" + str(result[1]), result[2], "tmall"])

    #Return it
    return finalList


if __name__ == '__main__':
    main()
# main()


#Sample Data
#resultList = [['【4+64G低至799】Xiaomi/小米 红米6 ai双摄8核全面屏智能学生老人拍照青春手机正品官方旗舰店Redm7Xnote5', 799, 'Xiaomi', 'tmall'], ['【优惠300元】荣耀Magic2华为HONOR/荣耀 智能全面手机官网全新正品荣耀magic2新款青春手机官方旗舰店8xV20', 3799, 'Huawei', 'tmall'], ['【4日2日10点开售】Xiaomi/小米 Redmi Note 7 Pro 新品骁龙675索尼4800万智能拍照水滴屏手机官方旗舰店', 1599, 'Xiaomi', 'tmall'], ['【稀缺宝石蓝】Xiaomi/小米小米MIX 3滑盖全面屏旗舰骁龙845拍照游戏官方旗舰店正品米9mix3故宫版mix2sxr', 3299, 'Xiaomi', 'tmall'], ['【爆款直降】Xiaomi/小米 红米6a智能老人学生青春拍照手机小米8周年官方旗舰店正品双卡双待4G全网通note5', 599, 'Xiaomi', 'tmall'], ['【到手价1599元起】Xiaomi/小米 小米Max3全面屏大屏大电量游戏手机智能拍照手机官方旗舰店正品米9note7', 1699, 'Xiaomi', 'tmall'], ['【低至1299元】华为HONOR/荣耀10青春版V珍珠全面屏2400万AI自拍渐变色智能学生游戏拍照手机官方旗舰店网', 1399, 'Huawei', 'tmall'], ['Xiaomi/小米 小米9 SE 骁龙712水滴屏拍照智能手机4800万超广角三摄拍照手机小米官方旗舰店 屏幕指纹解锁8SE', 1999, 'Xiaomi', 'tmall'], ['【8+128GB到手2899起】Xiaomi/小米 小米8屏幕指纹版9全面屏拍照手机8小米官旗青春红米note7骁龙845透明版', 3199, 'Xiaomi', 'tmall'], ['【6+64G低至1499】Xiaomi/小米 小米8 青春版全面屏智能拍照游戏手机学生商务9官方旗舰店正品红米note7note5', 1399, 'Xiaomi', 'tmall'], ['【指定版本赠燃脂配件】华为HONOR/荣耀V20新品全视屏麒麟980处理器4800万AI摄影智能游戏学生手机V10官网', 2999, 'Huawei', 'tmall'], ['【4+64GB下单赠配件】华为HONOR荣耀8X全面大屏幕指纹解锁智能游戏青春学生新手机老年人电话机官方网旗舰店', 1399, 'Huawei', 'tmall'], ['【6+128G低至1699】Xiaomi/小米 小米8SE 全面屏拍照游戏智能手机AI双摄红米note7 小米官旗9 青春版6+64GB灰', 1999, 'Xiaomi', 'tmall'], ['Apple/苹果 iPhone 8', 5099, 'Apple', 'tmall'], ['【新品现货速抢！】Xiaomi/小米 Redmi 7 红米7 骁龙632八核双摄智能拍照水滴屏手机 官方旗舰正品', 799, 'Xiaomi', 'tmall'], ['【高颜值+大流量】Xiaomi/小米 小米Play 官方旗舰店 8周年青春版全面屏双卡青春智能拍照游戏手机红米6pro', 1099, 'Xiaomi', 'tmall'], ['【现货开售】Xiaomi/小米 Redmi 红米Note7 骁龙660智能4800万拍照千元水滴屏pro手机9官方旗舰店正品note5', 999, 'Xiaomi', 'tmall'], ['【6+128G 2499元起】Xiaomi/小米小米8年度旗舰全面屏骁龙845指纹版智能拍照游戏手机旗舰官方', 2999, 'Xiaomi', 'tmall'], ['【8+256GB白色低至3399】Xiaomi/小米 MIX 2S全面屏骁龙845双摄手机智能游戏商务AI双摄mix3', 3999, 'Xiaomi', 'tmall'], ['Apple/苹果 iPhone XS', 8699, 'Apple', 'tmall'], ['Apple/苹果 iPhone XR', 6499, 'Apple', 'tmall'], ['【领券低至2099元】华为HONOR/荣耀 10GT游戏V2400万AI摄影全面屏网通智能拍照手机官方旗舰店官网学生双卡', 2599, 'Huawei', 'tmall'], ['【4月2日10点开卖】Xiaomi/小米小米9 骁龙855全面屏索尼4800万三摄指纹拍照游戏手机官方旗舰NFC王源代言', 2999, 'Xiaomi', 'tmall'], ['【爆款钜惠】Xiaomi/小米 6X智能AI双摄拍照学生老人青春手机小米8官方旗舰店正品双卡双待红米note7', 1799, 'Xiaomi', 'tmall'], ['GalaxyS10+SM-G9750855IP684G', 6999, 'Samsung', 'tmall'], ['GalaxyS10SM-G9730855IP684G', 5999, 'Samsung', 'tmall'], ['GalaxyS10eSM-G9700855IP684G', 4999, 'Samsung', 'tmall'], ['300GALAXYNote9SM-N96006+128GB/8+512GBSpen4G', 6599, 'Samsung', 'tmall'], ['300GALAXYNote9SM-N96008+512GBSpen4G', 8599, 'Samsung', 'tmall'], ['300GalaxyS9+SM-G9650/DS845IP684G', 5499, 'Samsung', 'tmall'], ['300GalaxyS9SM-G9600/DS845IP684G', 4799, 'Samsung', 'tmall'], ['GALAXYS8SM-G95004+64GB4G', 2999, 'Samsung', 'tmall'], ['GalaxyS8+SM-G95506+128GB4G', 3799, 'Samsung', 'tmall']]
# apple = [['https://detail.tmall.com/item.htm?id=579791278840', 'Apple'],
    #          ['https://detail.tmall.com/item.htm?id=577249277344', 'Apple'],
    #          ['https://detail.tmall.com/item.htm?id=558420556696&scene=taobao_shop', 'Apple']]
    # huawei = [['https://detail.tmall.com/item.htm?id=581727960031&scene=taobao_shop', 'Huawei'],
    #           ['https://detail.tmall.com/item.htm?id=567332753408&scene=taobao_shop', 'Huawei'],
    #           ['https://detail.tmall.com/item.htm?id=575984231019&scene=taobao_shop', 'Huawei'],
    #           ['https://detail.tmall.com/item.htm?id=579196707747&scene=taobao_shop', 'Huawei'],
    #           ['https://detail.tmall.com/item.htm?id=583857290585&scene=taobao_shop', 'Huawei']]
    # xiaomi = [['https://detail.tmall.com/item.htm?id=579914211622&scene=taobao_shop', 'Xiaomi'],
    #           ['https://detail.tmall.com/item.htm?id=570133905140&scene=taobao_shop', 'Xiaomi'],
    #           ['https://detail.tmall.com/item.htm?id=566510433862&scene=taobao_shop', 'Xiaomi'],
    #           ['https://detail.tmall.com/item.htm?id=567679236534&scene=taobao_shop', 'Xiaomi'],
    #           ['https://detail.tmall.com/item.htm?id=572473824056&scene=taobao_shop', 'Xiaomi'],
    #           ['https://detail.tmall.com/item.htm?id=573627357978&scene=taobao_shop', 'Xiaomi'],
    #           ['https://detail.tmall.com/item.htm?id=577610489452&scene=taobao_shop', 'Xiaomi'],
    #           ['https://detail.tmall.com/item.htm?id=577345730738&scene=taobao_shop', 'Xiaomi'],
    #           ['https://detail.tmall.com/item.htm?id=584384110633&scene=taobao_shop', 'Xiaomi'],
    #           ['https://detail.tmall.com/item.htm?id=589192455077&scene=taobao_shop', 'Xiaomi'],
    #           ['https://detail.tmall.com/item.htm?id=586768982581&scene=taobao_shop', 'Xiaomi'],
    #           ['https://detail.tmall.com/item.htm?id=570279488000&scene=taobao_shop', 'Xiaomi'],
    #           ['https://detail.tmall.com/item.htm?id=569705565098&scene=taobao_shop', 'Xiaomi'],
    #           ['https://detail.tmall.com/item.htm?id=584654464963&scene=taobao_shop', 'Xiaomi'],
    #           ['https://detail.tmall.com/item.htm?id=588763869289&scene=taobao_shop', 'Xiaomi'],
    #           ['https://detail.tmall.com/item.htm?id=589049441294&scene=taobao_shop', 'Xiaomi']]
