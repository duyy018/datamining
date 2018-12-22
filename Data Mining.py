#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from bs4 import BeautifulSoup as soup
from selenium import webdriver

import re
import time
import csv
import math

opening = 0
menu = 0
menu2= 0
menu3= 0
link = "kosong"
pd   = 0
cari = "unja"

def scraping(link , pd):
    progress = 4
    print("\n\n")
    print("2%  Mebuka Browser")
    con2 = webdriver.Chrome()
    #link lalu cetak link
    #print(link)
    print("4%  Melakukan Koneksi Ke link")
    con2.get(link)
    z=0
    while z < pd:
        if progress >=6:
            
            print(str(round(z / pd * 100)-5)+"% Scroll Web dan Scraping Ulang")
        #scroll kebawah
        con2.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #waktu tunggu
        time.sleep(2)

        #convert ke html
        page2 = soup(con2.page_source, "html.parser")
        #memilih data yg diambil
        p2 = page2.findAll("li", {"data-item-type":"tweet"})
        
        if progress >=6:
            print(str(round(z / pd * 100)-3)+"% Berhasil mendapatkan Data Sebanyak : "+str(len(p2)))
        #print banyak data
        if progress == 4:
            print("6%  Berhasil mendapatkan Data Sebanyak : "+str(len(p2)))
            progress =6
        z = len(p2)
    print("99% Cetak data html 10 huruf pertama")
    print(page2.prettify()[1:15])
    print("-----Scraping Selesai-----")
    return p2


def pembobotantfidf (p2):
    pcari = cari.replace(" ","").split(",")
    #print(pcari)
    
    print("1%  Membuat Data Csv")
    #buat file csv
    namafile = "Desktop\Datamining.csv"
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
        #print(pnama+" | "+idnama+"\n"+tweet+"\n")
        af.write(pnama+","+idnama+","+ptweet)
    
        kalimat = ptweet.lower().replace("."," ").replace(","," ").replace(":"," ").split(" ")
        for c in range(len(pcari)):
            banyak = 0
            for i in range(len(kalimat)):
                if pcari[c] in kalimat[i]:
                    banyak = banyak +1
            #print(pcari[c]+" : "+str(banyak))
            af.write(","+str(banyak))
    
        af.write("\n")
    af.close()

    #Cari File
    with open('Desktop\Datamining.csv', newline='') as csvfile:
        data1 = list(csv.reader(csvfile))

    #buat file csv bobot
    namafile = "Desktop\Datamining.csv"
    bf = open(namafile, "w+")
    #header
    column="df,D/df,log(D/df),log(D/df)+1"
    bf.write(column)
    for h in range(len(data1)-1):
        bf.write(",w"+str(h+1))
    bf.write("\n")

    #cari D   
    d = len(data1)-1
    #print("D : "+str(d))

    #cari Df
    for j in range(len(data1[0])):
        df = 0
        if j > 2 :
            for i in range(len(data1)):
                if data1[i][j] != '0':
                    df = df+1
            df=df-1
            #print("Df ke-"+str(j)+" : "+str(df))
        
            #cari D/df
            if df != 0:
                ddf = d / df
            else:
                ddf = 0
            #print("D/df : "+str(ddf))
        
            #cari log D/df
            if ddf !=0:
                logddf = round(math.log(ddf ,10), 2)
                #print("log(D/Df) : "+str(logddf))
            if ddf == 0:
                logddf = 0
            
            #ldf + 1
            ldf1 = round(logddf + 1 , 2)
            #print("log(D/Df) + 1  : "+str(ldf1))
        
            bf.write(str(df)+","+str(round(ddf,2))+","+str(logddf)+","+str(ldf1))
            # W
            for k in range(len(data1)):
                w = 0.0
                if k > 0 :
                    w = int(data1[k][j]) * ldf1
                    #print("W-d"+str(k)+" : "+str(w))
                    bf.write(","+str(w))
            #print("\n")
            bf.write("\n")
    bf.close()
    
    #Cari File
    with open('Desktop\Datamining.csv', newline='') as csvfile:
        data2 = list(csv.reader(csvfile))
    
    #buat file csv bobot akhir
    namafilec = "Desktop\Datamining.csv"
    cf = open(namafilec, "w+")
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
    cf.write(",Bobot_Dokumen\n")
    
    #copy data ke data mining.csv
    for c in range(len(data1)):
        if c > 0:
            sumd = 0.0
            for d in range(len(data1[0])):
                if d == 0:
                    cf.write(data1[c][d])
                if d > 0:
                    cf.write(","+data1[c][d])
    
            #copy bobot ke data mining csv
            for d in range(len(data2)):
                if d > 0:
                    sumd = sumd + float(data2[d][c+3])
                    cf.write(","+data2[d][c+3])
            cf.write(","+str(round(sumd, 2))+"\n")

    #copy df , D/df , log(D/df) , log(D/df)+1
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
    cf.close()
    print("100% Pembobotan Dokumen Selesai\n\nSilahkan Buka DataMining.csv yang ada di Desktop Anda\n\n\n")


while menu != 9:
    if opening == 0:
        print("\n\n                       :hdy.                      \n                       +ddd.                      \n                      `ddddo                      \n                       yddd:                      \n    .-/+sssso/-        :ddh        `-/+oo+/-.     \nyddddddddddddddd+.     -ddd      :sdddddddddddhyhs\n-hddddddddddddddddo` `-+ddd-`  :hdddddddddddddddd-   TWEET MINING V.2.1 CLI\n `hddddddddddddddddd/dddddddd/yddddddddddddddddd.    SISTEM INFORMASI - UNIVERSITAS JAMBI\n  `/hdddddddddddddddddddddddhdddddddddddddddddo-     by : @Duyy018\n    `/oo+oydddddddddddddddddddddddddddddsssso.    \n           `````:ddddddddddddddddo.----           \n                :ddddddddddddddddo                \n               /ydddddddddddddddds:               \n              .dddddddddddddddddddd/              \n               sddddddddddddddddddh.              \n                `oddddddddddddddh-`               \n                  oddddddddddddh.                 \n                 `+ydddddddddddo.                 \n                  `:oyh-...hyo:`                  \n")
        opening = 1
    if link != "kosong":
        print("Link Anda : "+link)
    if pd != 0:
        print("Panjang data yang ingin anda ambil lebih dari : "+str(pd))
    if cari != "unja":
        print("Kata yang ingin dicari : "+cari.replace(","," "))
        
    print("1.Instalasi \n2.Web Scraping \n3.Lakukan Mining \n8.ChangeLog \n9.Keluar Aplikasi\n")
    menu = int(input("Pilih Menu : "))
    
    if menu == 1:
        print("Untuk Menjalankan Aplikasi ini anda harus menginstal\n ->Selenium\n     pip install selenium\n ->Chrome *Terbaru\n     https://dl.google.com/chrome/install/latest/chrome_installer.exe\n ->Download Chrome Driver\n     https://sites.google.com/a/chromium.org/chromedriver/downloads\n     dan Extract di directory Python.Exe\n     Biasanya di\n     C:-Users-Duyy18-AppData-Local-Programs-Python")
    
    if menu == 2:
        print("1.Tweet Scraping\n8.Kembali\n9.Keluar Aplikasi\n")
        menu2 = int(input("Pilih Menu : "))
        while menu2 !=8:
            if menu2 == 1:
                link = input("Salin dan Tempel link twitter anda disini : ")
                pd = int(input("Banyak Data yang ingin diambil lebih dari : "))
                p2 = scraping(link, pd)
                print("\n\nDidapatkan Data Sebanyak : "+str(len(p2)))
                menu2 =8
            if menu2 == 9:
                menu2= 8
                menu = 9
            
        
    if menu == 3:
        while menu3 != 8:
            print("1.Pembobotan Tf/idf\n8.Kembali\n9.Keluar Aplikasi\n")
            menu3 = int(input("Pilih Menu : "))
            if menu3 == 1:
                if link == "kosong":
                    print("Masukan Link Terlebih dahulu !!")
                if pd == 0:
                    print("Masukan Panjang data Terlebih dahulu !!")
    
                if link != "kosong":
                    if pd != 0:
                        print("Masukan Kata yang ingin Dicari\njika kata lebih dari satu sisipkan , ditiap kata | contoh : unja,si")
                        cari = input("Kata yang ingin dicari : ")
                        if cari != "unja":
                            pembobotantfidf(p2)
            if menu3 == 9:
                menu3= 8
                menu = 9
    if menu == 8:
        print("  -Menu Lebih Sederhana\n  -Penambahan Koding Scraping\n  -Penambahan Koding Pembobotan Dokumen")
    if menu == 9:
        print ("\n\n----Semoga Aplikasi ini Bermanfaat untuk Anda :)----")
    print("\n\n\n")
    
    
    
    
    

