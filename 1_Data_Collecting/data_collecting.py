# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 01:06:04 2023

@author: veli1
"""

import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup

# gerekli listeler
url_list = []
prices_list = []
propTitles = []
propValues = []

# özelliklerin çekilmesi
for i in range(1, 75):  # 2 yerine sayfa sayısı gelmeli
    url = "https://www.trendyol.com/laptop-x-c103108?pi=" + str(i)
    r = requests.get(url)
    source = BeautifulSoup(r.content, "lxml")

    urls = source.find_all(
        "div", attrs={"class": "p-card-chldrn-cntnr card-border"})
    for url in urls:
        url_laptop = "https://www.trendyol.com/" + url.a.get("href")
        url_list.append(url_laptop)
        # print(url_laptop)

        # Her bir URL için ayrı ayrı istek yapma
        r_phone = requests.get(url_laptop)
        source_phone = BeautifulSoup(
            r_phone.content, "lxml")  # veri içerğini çekme

        properteis = source_phone.find_all(
            "li", attrs={"class": "detail-attr-item"})
        for prop in properteis:
            prop_title = prop.find("span").text
            prop_value = prop.find("b").text
            propTitles.append(prop_title)
            propValues.append(prop_value)
            # print(propTitles,propValues)

    prices = source.find_all("div", attrs={"class": "prc-box-dscntd"})
    for price in prices:
        prices_list.append(price.text)
        # print(price.text)


print(str(len(url_list)) + "adet link bulundu")
print(str(len(prices_list)) + "adet fiyat bulundu")
print(str(len(propTitles)) + "adet özellik ba bulundu")
print(str(len(url_list)) + "adet link bulundu")
# %%
#Url ve fiyatları bir data frame yazma
df_urls = pd.DataFrame()
df_urls["urls"] = url_list
df_urls["prices"] = prices_list
df_urls.head()
#%%
df_urls.head()
# %%
#Bulunan veri sayısı
laptop = len(url_list)
print(laptop)
#%%
#Bulunan özellik başlıklarının benzersizlerini bulma
columns = np.array(propTitles)
columns = np.unique(columns)
#%%
#Başlıkları kullanarak url ve fiyat ile birlikte yeni bir data frame oluşturma
df = pd.DataFrame(columns=columns)
df["url"] = url_list
df["price"] = prices_list

#%%
#Oluşturulan data frame gösterme
df.head()


#%%
#Data frame'i kullanarak bütün verileri çekme ve sütunlara yazdırma
for i in range(0, laptop):
    url = df['url'].loc[i]
    r = requests.get(url)
    source = BeautifulSoup(r.content, "lxml")
    
    properties = source.find_all(
        "li", attrs={"class": "detail-attr-item"})
    
    for prop in properties:
        prop_title = prop.find("span").text
        prop_value = prop.find("b").text
        print(prop_title + prop_value)
        df[prop_title].loc[i] = prop_value


#%%
df.head()
#%%
#Data frame'i csv formatına çevirip kaydetme
df.to_csv("laptop_trendyol_data3.csv",index=False)

#%%
df.columns

























