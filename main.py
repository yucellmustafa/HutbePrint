import os
from selenium import webdriver
import json
from time import sleep
import chromedriver_autoinstaller

drVer = str(chromedriver_autoinstaller.get_chrome_version())
drVer = drVer[0:drVer.index(".")]
hutbeler = [[],[],[]]

def printHutbeler(hutbeler):
    print(f"""
 NO |   TARIH    |              HUTBE ADI
-----------------------------------------------------------
 1  | {hutbeler[0][0]} | {hutbeler[0][1]}
 2  | {hutbeler[1][0]} | {hutbeler[1][1]}
 3  | {hutbeler[2][0]} | {hutbeler[2][1]}
""")

def createDr(headless):
    options = webdriver.ChromeOptions()
    settings = {
    "recentDestinations": [{
        "id": "Default",
        "origin": "local",
        "account": "",
    }],
    "selectedDestinationId": "Default",
    "version": 2
    }
    prefs = {'printing.print_preview_sticky_settings.appState': json.dumps(settings)}
    options.add_experimental_option('prefs', prefs)
    options.add_argument('--kiosk-printing')
    options.add_argument('--log-level=3')
    options.set_headless(headless)

    if(os.name == "nt"):
        return webdriver.Chrome(f'./{drVer}/chromedriver.exe',options=options)
    else:
        return webdriver.Chrome(f'./{drVer}/chromedriver',options=options)

def exceptPrint(uyari):
    print(uyari)
    input("Kapatmak için 'enter'a basınız...")
    exit()

def main():
    try:
        chromedriver_autoinstaller.install("./")
    except:
        exceptPrint("'chromedriver' güncellenemedi. Internet bağlantınızı kontrol edin !")

    try:      
        dr = createDr(True)
    except:
        exceptPrint("'chromedriver' bulunamadı !")

    try:
        dr.minimize_window()
        dr.get("https://dinhizmetleri.diyanet.gov.tr/kategoriler/yayinlarimiz/hutbeler/t%C3%BCrk%C3%A7e")

        for i in [1,2,3]:
            hutbeler[i-1].append(dr.find_element_by_xpath(f'/html/body/form/div[5]/div/div[2]/div/div/span/div[3]/div/div/div/div/div/div/div[2]/table/tbody/tr/td/table/tbody/tr[{i}]/td[2]/span').text) #Tarihleri alıyor

            hutbeler[i-1].append(dr.find_element_by_xpath(f'/html/body/form/div[5]/div/div[2]/div/div/span/div[3]/div/div/div/div/div/div/div[2]/table/tbody/tr/td/table/tbody/tr[{i}]/td[3]').text) #Hutbe Adı alıyor

            hutbeler[i-1].append(dr.find_element_by_xpath(f'/html/body/form/div[5]/div/div[2]/div/div/span/div[3]/div/div/div/div/div/div/div[2]/table/tbody/tr/td/table/tbody/tr[{i}]/td[4]/a').text) #Hutbe link adı alıyor

        dr.quit()

        os.system('cls' if os.name == 'nt' else 'clear')
        printHutbeler(hutbeler)

        hutbeNo = 0
        while (hutbeNo < 1 or hutbeNo > 3):
            hutbeNo = int(input("Hutbe NO : "))

        dr = createDr(False)

        dr.minimize_window()
        dr.get(f'https://dinhizmetleri.diyanet.gov.tr/Documents/{hutbeler[hutbeNo-1][2]}.pdf')
        dr.execute_script("window.print();")
        
        sleep(5)

    except:
        exceptPrint("Internet Baglantı Sorunu !")

if __name__ == '__main__':
    main()