from url_crawl import serp_title_link,previous_page_link
from text_crawl import text_without_garbage


url_list = []
count = 1
#sleep = 0.1
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
    #print(url)
  
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
