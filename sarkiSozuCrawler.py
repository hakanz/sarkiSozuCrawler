import csv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
#201902
profile = webdriver.FirefoxProfile("kojqp3po.default")
driver = webdriver.Firefox(profile)
nereye = "sarkisozleri.txt"
sanatciUrls = {}

def getSanatciUrls():
    global sanatciUrls
    with open('sanatciListesi.csv',encoding="utf8") as csvdd:
        csvd = csv.reader(csvdd, delimiter=',')
        c = 0
        for row in csvd:
            if not c == 0:
                sanatciUrls[c] = row[1]
                c += 1
            else:
                c += 1
        return sanatciUrls

getirilecekSarkiSozuind = 0
ind = 0
i = 0
main = 0
sarkiSozuUrls = {}

def sarkiSozuLinkToplayici():
    global driver
    sarkiAdlari = driver.find_elements_by_tag_name('a')
    q = 0
    global i
    global sarkiSozuUrls
    global getirilecekSarkiSozuind
    for s in sarkiAdlari:
        if q >= 7:
            sarkiSozuUrls[i] = s.get_attribute("href")
            i += 1
        q += 1
    print(main,". sanatçının ",len(sarkiSozuUrls)," adet şarkı sözünü buldum hepsini cukkalıyorum.")
    getirilecekSarkiSozuind = 0
    i = 0
    q = 0
    sarkiSozuGetirici()
    
def sarkiSozuGetirici():
    global main
    global sanatciListesi
    global sarkiSozuUrls
    global getirilecekSarkiSozuind
    if not sarkiSozuBittiMi():
        driver.get(sarkiSozuUrls[getirilecekSarkiSozuind])
        div = driver.find_element_by_class_name('col-md-6')
        if div:
            print("#",getirilecekSarkiSozuind,"/",len(sarkiSozuUrls),": ",driver.title)
            if driver.current_url == sarkiSozuUrls[getirilecekSarkiSozuind]:
                with open(nereye,'a',encoding='utf8', errors='ignore') as dosya:
                    if div.text:
                        soz = div.text
                        soz = harfTemizlikcisi(soz)
                        if turkce_mi(soz) == 1:
                            if kelimeFiltresi(soz):
                                dosya.write(soz)
                                siradakiGelsin()
                            else:
                                print("Bu şarkı sözü türkçe ama kelime filtresinden geçemedi, yazmıyorum bunu.")
                                siradakiGelsin()
                        else:
                            print("Bu şarkı sözü türkçe değil, yazmıyorum bunu.")
                            siradakiGelsin()
                    else:
                        print("Bu şarkının sözünü alamadım, neyse devam.")
                        siradakiGelsin()
            else:
                print("[HATA]: URL: "+driver.current_url+" | Olması gereken: "+sarkiSozuUrls[getirilecekSarkiSozuind])
        else:
            print("[HATA]: Şarkı sözünü alamadım, bu sanatçının şarkı sözleri bitmediyse devam ediyorum.")
            siradakiGelsin()
    else:
        siradakiGelsin()

            
#Bu harfler varsa Türkçe'dir herhalde?
def turkce_mi(soz):
    turkceKarakterler = {"ı","İ","ğ","Ğ","ü","Ü","ş","Ş","ö","Ö","ç","Ç"} 
    tr = 0
    for ch in turkceKarakterler:
        if ch in soz:
            tr = tr+1
    if tr >= 3:
        return 1
    else:
        return 0

#Dini değerleri içeren şarkı sözlerini, ilahilerin ve deyişlerin eklenmesini istemiyorum. Ayrıca cinsel içerikli ve küfürlü şarkı sözlerini de filtreliyoruz.
def kelimeFiltresi(soz):
    kelimeler = {"nigga"," zenci "," kürt "," xx","wer"," yoq ","style","best"," yes "," yeah ","allah","mekke","medine","hazreti","hz.","kuran","muhammed"," pirim "," pir "," şah ","ilahe","sex"," amına "," siktim ", " sikeyim "," sikik ","aşq"," amk "} 
    il = 0
    for ch in kelimeler:
        if ch in soz.lower():
            il = il+1
    if il >= 2:
        return False
    else:
        return True

#Bazı noktalama işaretlerinin silinmesini istemiyorum. O yüzden böyle avel gibi uğraştım.
def harfTemizlikcisi(soz):
    sileyim = {"|","…","-","*","%","!","\"","'","£","#","^","+","$","é","€","\\","...","\½","\_","\}","\[","\]","\{","(",")"}
    soz = soz.replace("İzle ve Dinle","")
    soz = soz.replace("Şarkı Sözleri","")
    for karakter in sileyim:
        if karakter in soz:
            soz = soz.replace(karakter,"")
    return soz
               
def sarkiSozuBittiMi():
    global getirilecekSarkiSozuind
    global sarkiSozuUrls
    if getirilecekSarkiSozuind >= len(sarkiSozuUrls):
        return True
    else:
        return False
    
def sanatciListesiBittiMi():
    global sanatciUrls
    global main
    if main >= len(sanatciUrls):
        return True
    else:
        return False

def siradakiGelsin():
    global sanatciUrls
    global sarkiSozuUrls
    global main
    global getirilecekSarkiSozuind
    if sarkiSozuBittiMi():
        print(str(main)+". sanatçının şarkı sözleri bitti.")
        main += 1
        if not sanatciListesiBittiMi():
            print(str(main)+". sanatçıya geçiyorum.")
            driver.get(sanatciUrls[main])
            sarkiSozuUrls = {}
            getirilecekSarkiSozuind = 0
            sarkiSozuLinkToplayici()
        else:
            print("Tamamen bitti.")
            driver.close()
    else:
        getirilecekSarkiSozuind += 1
        sarkiSozuGetirici()
        
#Script başlatıldığında döngüyü ilk burası tetikliyor.
kacSanatci = len(getSanatciUrls())
if len(sanatciUrls) > 1000:
    print(str(len(sanatciUrls)) + " tane sanatçı URL'si CSV'den getirildi.")
    driver.get(sanatciUrls[1])
    print(driver.title)
    sarkiSozuLinkToplayici()
else:
    print("Bir sorun var, CSV'den sanatçılar getirilemedi.")
