import os
from selenium import webdriver
import json
from time import sleep

hutbeler = [[],[],[]]

def printHutbeler(hutbeler):
    print(f"""
 NO |   TARIH    |              HUTBE ADI
-----------------------------------------------------------
 1  | {hutbeler[0][0]} | {hutbeler[0][1]}
 2  | {hutbeler[1][0]} | {hutbeler[1][1]}
 3  | {hutbeler[2][0]} | {hutbeler[2][1]}
""")

def main():
    try:
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

        if(os.name == "nt"):
            dr = webdriver.Chrome('./chromedriver.exe',options=options)
        else:
            dr = webdriver.Chrome('./chromedriver',options=options)
            
    except:
        print("'chromedriver' bulunamadı !")
        input("Kapatmak için 'enter'a basınız...")
        exit()

    try:
        dr.minimize_window()
        dr.get("https://dinhizmetleri.diyanet.gov.tr/kategoriler/yayinlarimiz/hutbeler/t%C3%BCrk%C3%A7e")

        for i in [1,2,3]:
            hutbeler[i-1].append(dr.find_element_by_xpath(f'/html/body/form/div[5]/div/div[2]/div/div/span/div[3]/div/div/div/div/div/div/div[2]/table/tbody/tr/td/table/tbody/tr[{i}]/td[2]/span').text) #Tarihleri alıyor

            hutbeler[i-1].append(dr.find_element_by_xpath(f'/html/body/form/div[5]/div/div[2]/div/div/span/div[3]/div/div/div/div/div/div/div[2]/table/tbody/tr/td/table/tbody/tr[{i}]/td[3]').text) #Hutbe Adı alıyor

            hutbeler[i-1].append(dr.find_element_by_xpath(f'/html/body/form/div[5]/div/div[2]/div/div/span/div[3]/div/div/div/div/div/div/div[2]/table/tbody/tr/td/table/tbody/tr[{i}]/td[4]/a').text) #Hutbe link adı alıyor

        os.system('cls' if os.name == 'nt' else 'clear')

        printHutbeler(hutbeler)

        hutbeNo = 0
        while (hutbeNo < 1 or hutbeNo > 3):
            hutbeNo = int(input("Hutbe NO : "))

        dr.get(f'https://dinhizmetleri.diyanet.gov.tr/Documents/{hutbeler[hutbeNo-1][2]}.pdf')
        dr.minimize_window()
        dr.execute_script("window.print();")
        sleep(5)

    except:
        print("Internet Baglantı Sorunu !")
        input("Kapatmak için 'enter'a basınız...")
        exit()

if __name__ == '__main__':
    main()