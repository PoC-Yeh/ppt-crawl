import csv
import progressbar
import re
import requests
import time
import pickle
from bs4 import BeautifulSoup
from url_crawl import serp_title_link,previous_page_link
from text_crawl import text_without_garbage


domain = "https://www.ptt.cc/"
url = "https://www.ptt.cc/bbs/MakeUp/index.html"


url_list = []
count = 1
page_count = 0
bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength) 

while True:
    serp_url = requests.get(url).text
    soup = BeautifulSoup(serp_url, "html.parser")
    serp_title_link()
    page_count += 1 #bar
    bar.update(page_count)  #bar
    
    #break when the last page is finished
    if url == "https://www.ptt.cc//bbs/MakeUp/index1.html":
        break
    previous_page_link()
    url = previous_page_link()
    
    #write csv automatically after crawling every 500 pages
    if count < 500:
        count += 1
    elif count == 500:
        count = 1
        for_csv_url_list = []
        for i in url_list:
            list_list = []
            list_list.append(i)
            for_csv_url_list.append(list_list)

        f = open('ptt_makeup.csv', 'w')
        w = csv.writer(f)
        w.writerows(for_csv_url_list)

        f.close()
    



url_text_dict = {} 
with_keyword_text = {}


keyword = "資生堂"
save_count = 0
url_count = 0
bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)


for url in url_list:
    try:
        page_content = text_without_garbage(url)
        #print(page_content)
        url_text_dict[url] = page_content

        for sentence in page_content:
            if keyword in sentence:
                with_keyword_text[url] = page_content[3:]  #without meta data
                
        url_count += 1 #bar
        bar.update(url_count)  #bar

        if save_count < 500:
            save_count += 1

        elif save_count == 500:
            save_count = 1

            f = open('makeup_text_new.csv', 'w')
            w = csv.writer(f)
            w.writerows(url_text_dict.items())
            f.close()

            f2 = open('shiseido_text_new.csv', 'w')
            w2 = csv.writer(f2)
            w2.writerows(with_keyword_text.items())
            f2.close()
            
        if url_count % 2000 == 0:
            time.sleep(60*15)
    
    except AttributeError:
        continue
        

output1 = pickle.dump(new_url_text_dict, open("url_text_dict.txt", "wb"))
ouptput2 = pickle.dump(new_with_keyword_text, open("with_keyword_text.txt", "wb"))

