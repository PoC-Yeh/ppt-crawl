from bs4 import BeautifulSoup
import requests
import time
import csv
import progressbar 


domain = "https://www.ptt.cc/"
url = "https://www.ptt.cc/bbs/MakeUp/index.html"


url_list = []


def serp_title_link():
    serp_url = requests.get(url).text
    soup = BeautifulSoup(serp_url, "html.parser")
    title = soup.find_all("div", class_ = "title")
    for i in title:
        if i.find("a") != None:
            a = i.find("a").get("href")
            if domain in a:
                url_list.append(a)
            else:
                whole_a = domain + a
                url_list.append(whole_a)
        
#previous page url
def previous_page_link():
    previous = soup.find_all("a", class_ = "btn wide")[1]
    previous_url = domain + previous.get("href")
    return(previous_url)


count = 1
sleep = 0.1
page_count = 0
bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength) 

while True:
    serp_title_link()
    page_count += 1   #bar
    bar.update(page_count)  #bar
    
    previous_page_link()
    #break when the last page is finished
    if previous_page_link() == None:
        break
    url = previous_page_link()
    
    
    #time.sleep(sleep)
    #sleep += 0.01
    
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
    
    

print(url_list[-1])

#for i in url_list:
#    print(i)
