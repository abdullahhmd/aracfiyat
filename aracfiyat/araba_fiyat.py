import requests
from bs4 import BeautifulSoup



def piyasa(yil,araba_model):
    araba_model = araba_model.split(" ",1)
    model_son = ""
    for kelime in araba_model:
        model_son+=kelime+","
    if model_son[-1]==",":
        model_son = model_son[:-1]
    link = "https://www.arabam.com/ikinci-el?searchText="+model_son+"&minYear="+str(yil)+"&maxYear="+str(yil)
    istek = requests.get(link)
    fiyatlar = []
    kaynak = BeautifulSoup(istek.content,'lxml')

    fiyat_bul = kaynak.findAll("a",attrs={"class":"listing-price"})

    for a in fiyat_bul:
        fiyatlar.append(int(a.text[:-3].replace(".","")))
    if len(fiyatlar)>0:
        ortalama_fiyat = sum(fiyatlar)/len(fiyatlar)
        return int(ortalama_fiyat)
    else:
        return 0
