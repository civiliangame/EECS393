from bs4 import BeautifulSoup
import xlwt
import time
import requests


#A method that gets rid of undesirable characters in a string.
#If a character in str is not in the string acceptables, it will take it out.
def purgeString(str, acceptables):

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
    index = len(num)
    for i in len(num):
        if num[i] == ".":
            index = i
    return num[0:index]

#A method that will return all the phone name/price pairs for samsung phones
#It will return a list of lists.
def samsungScraper():
    print("here we go")

    #Go to the tmall listing with all the samsung products
    r = requests.get("https://samsung.tmall.com/")
    print("loaded")

    time.sleep(.5)
    soup = BeautifulSoup(r.content, "lxml")

    #Samsung phones are in the a tag with class attribute "jdbmc abs mcblack" for some reason.
    #I don't know why. Don't ask me. I'm just finding patterns and then using them.
    samsungphones = soup.find("a", {"class": "jdbmc abs mcblack"})

    #Go to the new page listing all the samsung phones that we just found.
    r = requests.get("https:" + str(samsungphones.get("href")))

    time.sleep(.5)
    soup = BeautifulSoup(r.content, "lxml")

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
        phonelist.append([phonename, phoneprice])

    #Return the phonelist
    return phonelist

#A method that will go through the huawei site of tmall and find the links for the specific phones listed
def huaweiScraper():
    print("here we go")

    #Go to the site with the requests library.
    r = requests.get("https://huawei.tmall.com/")
    print("loaded")
    time.sleep(.5)

    #Download the content
    soup = BeautifulSoup(r.content, "lxml")

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
                    ptlinks.append("https:" + str(a.get("href")))

    #We now have all the links that are listed for their phones. We can return it.
    return ptlinks



#A method that scrapes the info for iphones of tmall
def applescraper():
    print("here we go")
    #Go to Apple's page for tmall
    r = requests.get("https://apple.tmall.com/")
    print("loaded")
    soup = BeautifulSoup(r.content, "lxml")

    #Find the category that says "iphone". How nice of them to use English for the first time.
    iphones = soup.find("a", string="iPhone")
    #Find the link for iphones.
    iphones_link = "https:" + iphones.get("href")

    #Go to that newly discovered link.
    r = requests.get(iphones_link)
    soup = BeautifulSoup(r.content, "lxml")

    #A list that will hold the links for specific iphones on sale there.
    specific_iphones = []

    #Apparently that chinese word there means "buy".
    #How nice of them to make it very simple to find the listings for individual iphones.
    for phonelink in soup.find_all("a", string="购买"):
        #Get the url from this page and add it to the list
        url = str(phonelink.get("href"))
        specific_iphones.append(url)
    return specific_iphones

#A method that finds the urls of all phones listed on Xiaomi's tmall page.
#It was originally going to be LG phones, but Tmall doesn't have LG phones
#And amazon doesn't have xiaomi phones.
def xiaomiscraper():

    #Go to the link
    print("here we go")
    r = requests.get("https://xiaomi.tmall.com/")
    print("loaded")

    #Download the page source
    soup = BeautifulSoup(r.content, "lxml")

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
                    urls.append("https:" + detailedUrl)

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
                    urls.append("https:" + detailedUrl)

    #Now that we have a list of all urls, we can just return it.
    return urls

#A method that takes a specific listing page as input and returns the name/price as output.
def specific_phones(link):
    r = requests.get(link)
    source_code = str(r.content)

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
    soup = BeautifulSoup(r.content, "lxml")
    #It's conveniently located in a tag named meta with attribute name = "keywords"
    meta = soup.find("meta", {"name": "keywords"})
    #Get the name
    phonename = (meta.get("content"))

    #We now have a nice pairing of phonename and phoneprice.
    return[phonename, phoneprice]





