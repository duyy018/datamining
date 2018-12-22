#!/usr/bin/env python
# coding: utf-8
# APLIKASI DATA MINING TWITTER | By Wahyudi F1E116005 | ice.cyber018@gmail.com
# # Data Mining

#import
from bs4 import BeautifulSoup as soup
from selenium import webdriver
import re
import time
import csv
import math

print("\n\n                       :hdy.                      \n                       +ddd.                      \n                      `ddddo                      \n                       yddd:                      \n    .-/+sssso/-        :ddh        `-/+oo+/-.     \nyddddddddddddddd+.     -ddd      :sdddddddddddhyhs\n-hddddddddddddddddo` `-+ddd-`  :hdddddddddddddddd-   TWEET MINING\n `hddddddddddddddddd/dddddddd/yddddddddddddddddd.    UNIVERSITAS JAMBI\n  `/hdddddddddddddddddddddddhdddddddddddddddddo-     by : @Duyy018\n    `/oo+oydddddddddddddddddddddddddddddsssso.    \n           `````:ddddddddddddddddo.----           \n                :ddddddddddddddddo                \n               /ydddddddddddddddds:               \n              .dddddddddddddddddddd/              \n               sddddddddddddddddddh.              \n                `oddddddddddddddh-`               \n                  oddddddddddddh.                 \n                 `+ydddddddddddo.                 \n                  `:oyh-...hyo:`                  \n")

#buka koneksi
con2 = webdriver.Chrome()
#link lalu cetak link
html = input("Masukan Limk: ")
print(html)

#konek ke link
con2.get(html)

banyakdata = int(input("Data yang mau diambil lebih dari : "))
z=0
while z < banyakdata:
    #scroll kebawah
    con2.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #waktu tunggu
    #time.sleep(2)

    #convert ke html
    page2 = soup(con2.page_source, "html.parser")
    #cetak data html 10 hurf pertama
    #print(page2.prettify()[1:15])

    #memilih data yg diambil
    p2 = page2.findAll("li", {"data-item-type":"tweet"})

    #print banyak data
    print(len(p2))
    z = len(p2)


#kata yang dicari
cari = input("masukan kata yang ingin dicari | *batasi dengan koma : ")
pcari = cari.replace(" ","").split(",")
print(pcari)

#buat file csv
namafile = "data.csv"
af = open(namafile, "w")
#header
af.write("nama,id,tweet")

for a in range(len(pcari)):
    af.write(",tf"+pcari[a])

af.write("\n")
#masukan ke file csv
for kolom in p2:
    nama = kolom.find("span",{"class":"FullNameGroup"}).text.strip().replace("\u200f","")
    idnama = kolom.find("span",{"class":"username u-dir u-textTruncate"}).text.strip().replace("\u200f","")
    tweet = kolom.find("div",{"class":"js-tweet-text-container"}).text.strip().replace("\u200f","")
    pnama = re.sub('[^ a-zA-Z0-9]', '', nama)
    ptweet = re.sub('[^ a-zA-Z0-9]', '', tweet)
    print(pnama+" | "+idnama)
    af.write(pnama+","+idnama+","+ptweet)
    
    kalimat = ptweet.lower().replace("."," ").replace(","," ").replace(":"," ").split(" ")
    for c in range(len(pcari)):
        banyak = 0
        for i in range(len(kalimat)):
            if pcari[c] in kalimat[i]:
                banyak = banyak +1
        print(pcari[c]+" : "+str(banyak))
        af.write(","+str(banyak))
    af.write("\n")
    print("\n")
af.close()

#Cari File
with open('data.csv', newline='') as csvfile:
    data = list(csv.reader(csvfile))

#buat file csv bobot
namafile = "bobot.csv"
bf = open(namafile, "w")
#header
column="df,D/df,log(D/df),log(D/df)+1"
bf.write(column)
for h in range(len(data)-1):
    bf.write(",w"+str(h+1))
bf.write("\n")
    
#cari D   
d = len(data)-1
print("D : "+str(d))

#cari Df
for j in range(len(data[0])):
    df = 0
    if j > 2 :
        for i in range(len(data)):
            if data[i][j] != '0':
                df = df+1
        df=df-1
        print("Df ke-"+str(j)+" : "+str(df))
        
        #cari D/df
        if df != 0:
            ddf = d / df
        else:
            ddf = 0
        print("D/df : "+str(ddf))
        
        #cari log D/df
        if ddf !=0:
            logddf = round(math.log(ddf ,10), 2)
            print("log(D/Df) : "+str(logddf))
        if ddf == 0:
            logddf = 0
        
        #ldf + 1
        ldf1 = round(logddf + 1 , 2)
        print("log(D/Df) + 1  : "+str(ldf1))
        
        bf.write(str(df)+","+str(round(ddf,2))+","+str(logddf)+","+str(ldf1))
        # W
        for k in range(len(data)):
            w = 0.0
            if k > 0 :
                w = int(data[k][j]) * ldf1
                #print("W-d"+str(k)+" : "+str(w))
                bf.write(","+str(w))
        print("\n")
        bf.write("\n")
bf.close()

#open file data.csv
with open('data.csv', newline='') as csvfile:
    data1 = list(csv.reader(csvfile))
    
#open File bobot.csv
with open('bobot.csv', newline='') as csvfile:
    data2 = list(csv.reader(csvfile))
    
#buat file csv bobot akhir
namafilec = "datamining.csv"
cf = open(namafilec, "w")
#header
#copy header data.csv
for a in range(len(data1[0])):
    if a == 0:
        cf.write(data1[0][a])
    if a > 0 :
        cf.write(","+data1[0][a])
#menambahkan W kata yang dicari dari data.csv
for b in range(len(data1[0])):
    if b > 2 :
        cf.write(",W-"+data1[0][b])
cf.write("\n")

#copy data ke data mining.csv
for c in range(len(data1)):
    if c > 0:
        for d in range(len(data1[0])):
            if d == 0:
                cf.write(data1[c][d])
            if d > 0:
                cf.write(","+data1[c][d])
    
        #copy bobot ke data mining csv
        for d in range(len(data2)):
            if d > 0:
                cf.write(","+data2[d][c+3])
        cf.write("\n")

#copy df , D/df , log(D/df) , log(D/df)+1 ke datamining.csv
for e in range(len(data2[0])):
    if e < 4:
        for f in range(len(data2)):
            if f == 0 :
                cf.write(data2[f][e])
                for g in range(2):
                    cf.write(","+" ")
            if f > 0 :
                cf.write(","+data2[f][e])
        cf.write("\n")
        
#insert sumary ke data datamining.cs
cf.write("sum")
skip = len(data1[0])
for h in range(skip-1):
    cf.write(","+" ")
for m in range(len(data2)):
    if m > 0:
        sumary = 0.0
        for l in range(len(data2[0])):
            if l > 3 :
                sumary = sumary + float(data2[m][l])
        cf.write(","+str(round(sumary, 2)))
        print("Bobot kata ke-"+str(m)+" : "+str(round(sumary, 2)))
cf.write("\n")
cf.close()