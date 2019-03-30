import tmallscraper
import genericAmazonScraper
import xlwt

def main():

    #Get the data from Amazon
    amazonResultList = genericAmazonScraper.main()
    #Get the data from tmall
    tmallResultList = tmallscraper.main()

    print("Assimilation Complete")
    resultList = []

    #Copy the data over to one big list for easier processing
    for item in tmallResultList:
        resultList.append(item)
    for item in amazonResultList:
        resultList.append(item)

    print(resultList)

    #Write it to the excel sheet and I'm done
    book = xlwt.Workbook(encoding="utf-8")
    sheet1 = book.add_sheet("Sheet 1")

    sheet1.write(0, 0, "Phone Name")
    sheet1.write(0, 1, "Price")
    sheet1.write(0, 2, "Company Name")
    sheet1.write(0, 3, "Source")
    print(len(resultList))
    for i in range(0, len(resultList)):
        for j in range(0, 4):
            sheet1.write(i + 1, j, resultList[i][j])
    book.save("results.xls")


#SampleData
#resultList = [['【爆款钜惠】Xiaomi/小米 6X智能AI双摄拍照学生老人青春手机小米8官方旗舰店正品双卡双待红米note7', '元1799', 'Xiaomi', 'tmall'], ['【低至1299元】华为HONOR/荣耀10青春版V珍珠全面屏2400万AI自拍渐变色智能学生游戏拍照手机官方旗舰店网', '元1399', 'Huawei', 'tmall'], ['【8+128GB到手2899起】Xiaomi/小米 小米8屏幕指纹版9全面屏拍照手机8小米官旗青春红米note7骁龙845透明版', '元3199', 'Xiaomi', 'tmall'], ['【4+64G低至799】Xiaomi/小米 红米6 ai双摄8核全面屏智能学生老人拍照青春手机正品官方旗舰店Redm7Xnote5', '元799', 'Xiaomi', 'tmall'], ['【稀缺宝石蓝】Xiaomi/小米小米MIX 3滑盖全面屏旗舰骁龙845拍照游戏官方旗舰店正品米9mix3故宫版mix2sxr', '元3299', 'Xiaomi', 'tmall'], ['【新品现货速抢！】Xiaomi/小米 Redmi 7 红米7 骁龙632八核双摄智能拍照水滴屏手机 官方旗舰正品', '元799', 'Xiaomi', 'tmall'], ['【爆款直降】Xiaomi/小米 红米6a智能老人学生青春拍照手机小米8周年官方旗舰店正品双卡双待4G全网通note5', '元599', 'Xiaomi', 'tmall'], ['【高颜值+大流量】Xiaomi/小米 小米Play 官方旗舰店 8周年青春版全面屏双卡青春智能拍照游戏手机红米6pro', '元1099', 'Xiaomi', 'tmall'], ['【6+64G低至1499】Xiaomi/小米 小米8 青春版全面屏智能拍照游戏手机学生商务9官方旗舰店正品红米note7note5', '元1399', 'Xiaomi', 'tmall'], ['【指定版本赠燃脂配件】华为HONOR/荣耀V20新品全视屏麒麟980处理器4800万AI摄影智能游戏学生手机V10官网', '元2999', 'Huawei', 'tmall'], ['Xiaomi/小米 小米9 SE 骁龙712水滴屏拍照智能手机4800万超广角三摄拍照手机小米官方旗舰店 屏幕指纹解锁8SE', '元1999', 'Xiaomi', 'tmall'], ['【现货速发】Xiaomi/小米 Redmi 红米Note7 骁龙660智能4800万拍照千元水滴屏pro手机9官方旗舰店正品note5', '元999', 'Xiaomi', 'tmall'], ['【到手价1599元起】Xiaomi/小米 小米Max3全面屏大屏大电量游戏手机智能拍照手机官方旗舰店正品米9note7', '元1699', 'Xiaomi', 'tmall'], ['【6+128G低至1699】Xiaomi/小米 小米8SE 全面屏拍照游戏智能手机AI双摄红米note7 小米官旗9 青春版6+64GB灰', '元1999', 'Xiaomi', 'tmall'], ['【4月2日10点开卖】Xiaomi/小米小米9 骁龙855全面屏索尼4800万三摄指纹拍照游戏手机官方旗舰NFC王源代言', '元2999', 'Xiaomi', 'tmall'], ['【6+128G 2499元起】Xiaomi/小米小米8年度旗舰全面屏骁龙845指纹版智能拍照游戏手机旗舰官方', '元2999', 'Xiaomi', 'tmall'], ['【4+64GB下单赠配件】华为HONOR荣耀8X全面大屏幕指纹解锁智能游戏青春学生新手机老年人电话机官方网旗舰店', '元1399', 'Huawei', 'tmall'], ['【优惠300元】荣耀Magic2华为HONOR/荣耀 智能全面手机官网全新正品荣耀magic2新款青春手机官方旗舰店8xV20', '元3799', 'Huawei', 'tmall'], ['【8+256GB白色低至3399】Xiaomi/小米 MIX 2S全面屏骁龙845双摄手机智能游戏商务AI双摄mix3', '元3999', 'Xiaomi', 'tmall'], ['【4日2日10点开售】Xiaomi/小米 Redmi Note 7 Pro 新品骁龙675索尼4800万智能拍照水滴屏手机官方旗舰店', '元1599', 'Xiaomi', 'tmall'], ['【领券低至2099元】华为HONOR/荣耀 10GT游戏V2400万AI摄影全面屏网通智能拍照手机官方旗舰店官网学生双卡', '元2599', 'Huawei', 'tmall'], ['Apple/苹果 iPhone 8', '元5099', 'Apple', 'tmall'], ['Apple/苹果 iPhone XS', '元8699', 'Apple', 'tmall'], ['Apple/苹果 iPhone XR', '元6499', 'Apple', 'tmall'], ['GalaxyS10+SM-G9750855IP684G', '元6999', 'Samsung', 'tmall'], ['GalaxyS10SM-G9730855IP684G', '元5999', 'Samsung', 'tmall'], ['GalaxyS10eSM-G9700855IP684G', '元4999', 'Samsung', 'tmall'], ['300GALAXYNote9SM-N96006+128GB/8+512GBSpen4G', '元6599', 'Samsung', 'tmall'], ['300GALAXYNote9SM-N96008+512GBSpen4G', '元8599', 'Samsung', 'tmall'], ['300GalaxyS9+SM-G9650/DS845IP684G', '元5499', 'Samsung', 'tmall'], ['300GalaxyS9SM-G9600/DS845IP684G', '元4799', 'Samsung', 'tmall'], ['GALAXYS8SM-G95004+64GB4G', '元2999', 'Samsung', 'tmall'], ['GalaxyS8+SM-G95506+128GB4G', '元3799', 'Samsung', 'tmall'], ['LG Electronics LG V40 Factory Unlocked Phone - 6.4Inch Screen - 64GB - Black (U.S. Warranty)', '$949.99', 'LG', 'Amazon'], ['LG V35 ThinQ with Alexa Hands-Free – Prime Exclusive Phone – Unlocked – 64 GB – Aurora Black', '$649.99', 'LG', 'Amazon'], ['LG Electronics G7 ThinQ Factory Unlocked Phone - 6.1" Screen - 64GB - Aurora Black (U.S. Warranty)', '$618.50', 'LG', 'Amazon'], ['LG Electronics K8 2018 Factory Unlocked Phone - 5 Inch Screen - 16GB - Morrocan Blue (U.S. Warranty)', '$119.93', 'LG', 'Amazon'], ['LG Electronics K30 Factory Unlocked Phone, 16GB (U.S. Warranty) - 5.3" - Black', '$140.00', 'LG', 'Amazon'], ['Samsung Galaxy S10+ Factory Unlocked Phone with 1TB (U.S. Warranty), Ceramic White', '$1,599.99', 'Samsung', 'Amazon'], ['Samsung Galaxy S10 Factory Unlocked Phone with 512GB (U.S. Warranty), Prism White', '$1,149.99', 'Samsung', 'Amazon'], ['Apple iPhone XS Max (64GB) - Silver - [works exclusively with Simple Mobile]', '$1,099.99', 'Apple', 'Amazon'], ['Apple iPhone XS Max (64GB) - Gold - [works exclusively with Simple Mobile]', '$1,099.99', 'Apple', 'Amazon'], ['Apple iPhone XS Max (64GB) - Space Gray- [works exclusively with Simple Mobile]', '$1,099.99', 'Apple', 'Amazon'], ['Apple iPhone XS (64GB) - Gold - [works exclusively with Simple Mobile]', '$999.99', 'Apple', 'Amazon'], ['Apple iPhone XS (64GB) - Space Gray - [works exclusively with Simple Mobile]', '$999.99', 'Apple', 'Amazon'], ['Apple iPhone XR (64GB) - Black - [works exclusively with Simple Mobile]', '$749.00', 'Apple', 'Amazon'], ['Apple iPhone XR (64GB) - (PRODUCT)RED [works exclusively with Simple Mobile]', '$749.99', 'Apple', 'Amazon'], ['Apple iPhone XR (64GB) - Black - [works exclusively with Simple Mobile]', '$749.00', 'Apple', 'Amazon'], ['Apple iPhone XR (64GB) - Black - [works exclusively with Simple Mobile]', '$749.00', 'Apple', 'Amazon'], ['Apple iPhone X (64GB) - Silver - [works exclusively with Simple Mobile]', '$899.00', 'Apple', 'Amazon'], ['Apple iPhone 8 (64GB) - Silver - [works exclusively with Simple Mobile]', '$649.00', 'Apple', 'Amazon'], ['Apple iPhone 7 Plus (32GB) - Black - [works exclusively with Simple Mobile]', '$399.99', 'Apple', 'Amazon'], ['Apple iPhone 7 Plus (32GB) Silver - [Simple Mobile]', '$399.99', 'Apple', 'Amazon'], ['Apple iPhone 7 (32GB) - Black - [works exclusively with Simple Mobile]', '$299.99', 'Apple', 'Amazon'], ['Apple iPhone 7 (32GB) - Gold - [works exclusively with Simple Mobile]', '$299.99', 'Apple', 'Amazon'], ['Apple iPhone 6s Plus (32GB) - Rose Gold [Locked to Simple Mobile Prepaid]', '$299.99', 'Apple', 'Amazon'], ['Apple iPhone 6S (32GB) - Space Gray - [works exclusively with Simple Mobile]', '$199.99', 'Apple', 'Amazon'], ['Huawei Mate SE Factory Unlocked 5.93” - 4GB/64GB Octa-core Processor| 16MP + 2MP Dual Camera| GSM Only |Grey (US Warranty)', '$219.99', 'Huawei', 'Amazon'], ['Huawei Mate 10 Pro Unlocked Phone, 6" 6GB/128GB, AI Processor, Dual Leica Camera, Water Resistant IP67, GSM Only - Titanium Gray (US Warranty)', '$489.98', 'Huawei', 'Amazon'], ['Huawei Mate 10 Pro Unlocked Phone, 6" 6GB/128GB, AI Processor, Dual Leica Camera, Water Resistant IP67, GSM Only - Midnight Blue (US Warranty)', '$489.00', 'Huawei', 'Amazon'], ['Huawei Mate 10 Pro Unlocked Phone, 6" 6GB/128GB, AI Processor, Dual Leica Camera, Water Resistant IP67, GSM Only - Mocha Brown (US Warranty)', '$497.00', 'Huawei', 'Amazon'], ['Huawei Mate 10 Porsche Design Factory Unlocked 256GB Android Smartphone Diamond Black', '$728.99', 'Huawei', 'Amazon']]
