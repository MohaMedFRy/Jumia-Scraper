# -*- coding: utf-8 -*-
"""
Created on Sun Aug  8 18:12:32 2021

@author: MohaMedFRy
"""

import requests 
from bs4 import BeautifulSoup
import csv 
from itertools import zip_longest


def Scarp(prod):
    cnt= 1
    product_name = []
    
    rating = []
    price = []
    product_details =[]
    key_features = []
               
    cur_link =f'https://www.jumia.com.eg/catalog/?q={prod}&page={cnt}#catalog-listing'
    result = requests.get(cur_link)
    src = result.content
    soup = BeautifulSoup(src , 'lxml')
    
    last_page = soup.find('a',{'aria-label' : "Last Page"})
    last = "https://www.jumia.com.eg" +last_page.attrs['href']
    #print(cur_link)
    while True:    
        links = []
        print("page : ", cnt)
        cur_link =f'https://www.jumia.com.eg/catalog/?q={prod}&page={cnt}#catalog-listing'
        result = requests.get(cur_link)
        src = result.content
        soup = BeautifulSoup(src , 'lxml')
        
        
        
        link = soup.find_all("article", {'class' : 'prd _fb col c-prd'})
        
        for i in range(len(link)):
            s = "https://www.jumia.com.eg" + link[i].find('a').attrs['href']
            links.append(s)
        
        sz = 1 
        for i in links:
            print("block : ", sz)
            sz += 1
            
            result = requests.get(i)
            src = result.content
            soup = BeautifulSoup(src, 'lxml')
            
            products = soup.find('h1', {'class' : '-fs20 -pts -pbxs'})
            rate = soup.find('div', {'class' : 'stars _s _al'})
            prices = soup.find('span' , {'class' : '-b -ltr -tal -fs24'})
            det = soup.find('div', {'class' : 'markup -mhm -pvl -oxa -sc'})
            try : 
                feat = soup.find('div', {'class' : 'markup -pam'}).find('ul').find_all('li')
        
                if feat: 
                    s = "" 
                    for j in feat:
                        s += " #"
                        s += j.text.replace("\n", " ")
                        key_features.append(s)
                else: key_features.append("NA")
            except:
                try: 
                    feat = soup.find('div', {'class' : 'markup -pam'})
                    key_features.append(feat.text)
                except:
                    key_features.append("NA")
            
            if products:    product_name.append(products.text)
            else: product_name.append("NA") 
            
          
            if rate:    rating.append(rate.text)
            else:   rating.append("NA")
            
            if prices:    price.append(prices.text)
            else: price.append("NA")
            
            if det:     product_details.append(det.text)
            else:   product_details.append("NA")
        # print(last)
        # print(cur_link)
        if last == cur_link: break
        cnt+=1
        #print (len(links))

    print("Scraping Done")
    file_list = [product_name, rating, price, product_details, key_features]
    exported = zip_longest(*file_list)
            
    with open("F:\Scraping\Jumia\Data From Jumia.csv", 'w' ,encoding='utf-8') as file:
        wr = csv.writer(file)
        wr.writerow(['Product Name', 'Rating', 'Price', 'Product Details', 'Key Features'])
        wr.writerows(exported)
    
          
    print("Done")

s = input("What kind of product needs to be search for it ? ")
Scarp(s)


