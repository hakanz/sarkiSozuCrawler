import json
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
profile = webdriver.FirefoxProfile("kojqp3po.default")
driver = webdriver.Firefox(profile)
#201902
sanatcilarUrl = "https://www.sarkisozleri.bbs.tr/sanatcilar"
nereye = "sarkisozleri.txt"

driver.get(sanatcilarUrl)

sanatciListesi = {}
sanatciUrls = {}
sanatciListindex = 0
sanatciListM = 0
toplamSarkiSozuCount = 0

def sanatciListGetir():
    global sanatciListesi
    global sanatciUrls
    global sanatciListindex
    global sanatciListM
    global toplamSarkiSozuCount
    sanatciL = driver.find_elements_by_tag_name('a')
    for hr in sanatciL:
        href = hr.get_attribute("href")
        if "sanatci" in href and not "sanatcilar" in href:
            sayi = hr.find_element_by_tag_name("span").text
            sanatciAdi = str(hr.text).replace(sayi,"")
            sanatciAdi = str(sanatciAdi).replace("\n","")
            toplamSarkiSozuCount = toplamSarkiSozuCount+int(sayi)
            sanatciListesi[sanatciListindex] = [sanatciAdi,href,sayi]
            #sanatciUrls[sanatciListindex] = href
            sanatciListindex = sanatciListindex+1
    print(len(sanatciListesi)," adet sanatçı sayfası ve ",str(toplamSarkiSozuCount)," adet şarkı sözü bulundu.")
    if not sanatciListM == 42: #42 sayfa var o yüzden böyle
        sanatciListM = sanatciListM+1
        driver.get(sanatcilarUrl+"/"+str(sanatciListM))
        sanatciListGetir()
    else:
        print("Sanatçı analizi bitti, toplamda ",len(sanatciListesi)," adet sanatçı ve ",str(toplamSarkiSozuCount)," adet şarkı sözü bulundu.")
        xmlOlustur(sanatciListesi)

def xmlOlustur(sanatciListesi):
    dosya = "sanatciListesi.xml"
    dosya2 = "sanatciListesi.json"
    dosya3 = "sanatciListesi.csv"
    dosya2 = open(dosya2,'a',encoding='utf8',errors='ignore')
    dosya2.write(json.dumps(sanatciListesi))
    i = 0
    xml = "<root>"
    csv = "id,url,sarkiSayisi,sanatciAdi\n"
    for url in sanatciListesi:
        print(sanatciListesi[i][1])
        csv += str(i)+","+sanatciListesi[i][1]+","+sanatciListesi[i][2]+","+sanatciListesi[i][0]+"\n"
        xml += "<sanatci id=\""+str(i)+"\" url=\""+sanatciListesi[i][1]+"\" sarkiCount=\""+sanatciListesi[i][2]+"\">"+sanatciListesi[i][0]+"</sanatci>"
        i = i+1
    xml += "</root>"
    with open(dosya,'a',encoding='utf8', errors='ignore') as dosya:
        dosya.write(xml)
    with open(dosya3,'a',encoding='utf8', errors='ignore') as dosya3:
        dosya3.write(csv)
sanatciListGetir()
#ilk sanatçı sayfasını aç
driver.get(sanatciListesi[0][1])
