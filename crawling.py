from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time
import csv
import pyperclip

from selenium.common.exceptions import NoSuchElementException
from urllib3 import add_stderr_logger
options = webdriver.ChromeOptions()
#options.add_argument('headless')

driver = webdriver.Chrome('./chromedriver.exe', options = options)
driver.implicitly_wait(3)
ENTER='/ue007'

# 에러시 부여할 딜레이(단위[초])
delay = 3

login=1

if login==1 :
    # 로그인
    driver.get('https://nid.naver.com/nidlogin.login')
    time.sleep(1)

    pyperclip.copy('hyunju990401') # 네이버 ID를 복붙하여 넣음
    driver.find_element_by_id('id').send_keys(Keys.CONTROL, 'v')
    time.sleep(1)

    pyperclip.copy('noether1882') # 네이버 PW를 복붙하여 넣음, 보안 주의
    driver.find_element_by_id('pw').send_keys(Keys.CONTROL, 'v')
    time.sleep(1)

    driver.find_element_by_id('log.login').click()
    time.sleep(1)

# 카페 정보
url = 'https://cafe.naver.com/joonggonara' # 크롤링 할 카페 주소
joonggonara_id = 10050146 # 크롤링 할 카페id

pages = 1000 # 크롤링할 페이지 수
menu_id=427 # buds pro
#menu_id = 749 #태블릿

# 카테고리 열기
driver.get(f'{url}?iframe_url=/ArticleList.nhn?search.clubid={joonggonara_id}%26search.menuid={menu_id}%26') #사이트 접속
time.sleep(2)
driver.switch_to.frame("cafe_main") # iframe으로 전환
driver.find_element_by_xpath('//*[@id="query"]').send_keys("에어팟 프로 미개봉")
driver.find_element_by_xpath('//*[@id="main-area"]/div[7]/form/div[3]/button').click()
driver.find_element_by_xpath('//*[@id="searchOptionSelectDiv"]/a').click()
driver.find_element_by_xpath('//*[@id="searchOptionSelectDiv"]/ul/li[1]/a').click()
driver.find_element_by_xpath('//*[@id="listSizeSelectDiv"]/a').click()
driver.find_element_by_xpath('//*[@id="listSizeSelectDiv"]/ul/li[7]/a').click()
author = []
author_num = []
written_time = []
title=[]
price=[]
length=[]
img=[]
deliver=[]
attend_num=[]
talk=[]
spam=[]
k = 0

board_list = []
board_urls = []

while k < 5: # for move to next page
    for l in range(1, 11):
        for i in range(1, 51):
            try: 
                problem=1
                spam_temp=2
                time.sleep(1)
                #작성 시간
                temp=driver.find_element_by_xpath(f'//*[@id="main-area"]/div[5]/table/tbody/tr[{i}]/td[3]').text
                if len(temp)==5:
                    now=time.localtime()

                    if len(str(now.tm_mon))==1:
                        mon="0"+str(now.tm_mon)
                    else: mon=str(now.tm_mon)

                    if len(str(now.tm_mday))==1:
                        mon="0"+str(now.tm_mday)
                    else: day=str(now.tm_mday)
            
                    temp=str(now.tm_year)+"."+mon+"."+day
                
            
                #제목
                title_temp=driver.find_element_by_xpath(f'//*[@id="main-area"]/div[5]/table/tbody/tr[{i}]/td[1]/div[2]/div/a').text
                

                if '워치' in title_temp or '2세대' in title_temp:
                    problem=0

                #작성 수, 가격, 그림 개수, 텍스트 글자
                target1 = driver # preserve driver element

                time.sleep(1)
                target = target1.find_element_by_xpath(f'//*[@id="main-area"]/div[5]/table/tbody/tr[{i}]/td[1]/div[2]/div/a')
                target.send_keys(Keys.CONTROL + "\n")
                driver.switch_to.window(driver.window_handles[1])
                
                time.sleep(1)
                
                driver.switch_to.frame("cafe_main")
                
                #가격
                price_temp=driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div/strong').text
                
                price_temp=''.join( x for x in price_temp if x not in ",원")


                if driver.find_element_by_xpath('/html/body/div/div/div/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/p/em').text=="완료":
                    spam_temp=0
                
            
                if int(price_temp)<120000 or int(price_temp)>300000:
                    problem=0

                if problem: 
                    #작성자
                    author_temp=driver.find_element_by_xpath('/html/body/div/div/div/div[2]/div[1]/div[2]/div/div[1]/div/a').text
                
                    #텍스트 길이
                    p=1
                    q=1
                    i=1
                    j=1
                    temp_length=0
                    img_count=0
                    temp_talk=1
                    temp_deliver=0
                    
                    
                    while(p):
                        try: 
                            driver.find_element_by_xpath(f'/html/body/div/div/div/div[2]/div[2]/div[1]/div[4]/div[1]/div/div/div[{j}]/div/div/div/p[1]/span')
                            print(driver.find_element_by_xpath(f'/html/body/div/div/div/div[2]/div[2]/div[1]/div[4]/div[1]/div/div/div[{j}]/div/div/div/p[1]/span').text)

                            while(q):
                                try: 
                                    is_text = driver.find_element_by_xpath(f'/html/body/div/div/div/div[2]/div[2]/div[1]/div[4]/div[1]/div/div/div[{j}]/div/div/div/p[{i}]/span').text
                                    temp_length+=len(is_text)
                                    if 'talk' in is_text or '톡' in is_text:
                                        temp_talk=0
                                    if '직거래' in is_text:
                                        temp_deliver=1
                                    i+=1
                                except: 
                                    q=0    
                        except:
                            try:
                                driver.find_element_by_xpath(f'/html/body/div/div/div/div[2]/div[2]/div[1]/div[4]/div[1]/div/div/div[{j}]/div/div/div/a/img')
                                img_count+=1

                            except: 
                                #print("Finish") 
                                p=0
                                
                        q=1
                        i=1
                        j+=1    

                    
                    #print("talk: ", temp_talk)               
                    #print("직거래 여부", temp_deliver)
                    
                    try: #작성자    
                        driver.find_element_by_xpath(f'/html/body/div/div/div/div[2]/div[1]/div[2]/div/div[1]/div/a').click() #작성자 클릭
                        time.sleep(1)
                        driver.find_element_by_xpath(f'/html/body/div/div/div/div[2]/div[1]/div[2]/div/div[1]/div/div/ul/li[1]/a').click() #게시글 보기 클릭
                        time.sleep(2)
                        author_num.append(driver.find_element_by_xpath(f'//*[@id="sub-tit"]/div[1]/div[2]/div/span[2]/em').text) #작성 수
                        attend_num.append(driver.find_element_by_xpath(f'/html/body/div[1]/div/div/div[1]/div[2]/div/span[1]/em').text)

                    except:
                        author_num.append(-1)
                        attend_num.append(-1)
                    
                    written_time.append(temp)
                    title.append(''.join( x for x in title_temp if x not in ","))
                    author.append(author_temp)   
                    length.append(temp_length)
                    img.append(img_count)
                    talk.append(temp_talk)       
                    deliver.append(temp_deliver)                 
                    price.append(price_temp)
                    spam.append(spam_temp)    

                else: 
                    written_time.append(temp)
                    title.append(''.join( x for x in title_temp if x not in ","))
                    author.append(-1)
                    length.append(-1)
                    img.append(-1)
                    talk.append(-1)       
                    deliver.append(-1)
                    author_num.append(-1)
                    attend_num.append(-1) 
                    price.append(price_temp)
                    spam.append(spam_temp)  

                driver.close() # close current tab
            
                driver.switch_to.window(driver.window_handles[0]) # focus on first tab
                #driver.refresh()
                try:
                    driver.switch_to.frame("cafe_main")  # re-enter iframe
                except:
                    continue
            except: 
                continue

        mod= l % 11 + 1 # 1 ~ 11
        if k == 0:
            if mod == 11:
                target = target1.find_element_by_xpath(f'//*[@id="main-area"]/div[7]/a[{mod}]')
                target.send_keys(Keys.CONTROL + "\n")
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                driver.switch_to.frame("cafe_main")
                k = k + 1
                continue
            
        elif k > 0:
            mod  = mod + 1 # 2 ~ 12
            if mod == 12:
                target = target1.find_element_by_xpath(f'//*[@id="main-area"]/div[7]/a[{mod}]')
                target.send_keys(Keys.CONTROL + "\n")
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                driver.switch_to.frame("cafe_main")
                k = k + 1
                continue
        driver.find_element_by_xpath(f'//*[@id="main-area"]/div[7]/a[{mod}]').click()

        print("current Mod number", mod, "print K number", k, "print l number", l)
        if k == 0:
            print("Current page number: ", (10*k + mod))
            
        else:
            print("Current page number: ", (10*k + mod) - 1)
        
        continue

temp_data=[title, written_time, author, author_num, price, length, img, attend_num, deliver, talk, spam]
                                          
print("게시글 제목: ", title) 
print("작성 시간: ", written_time)
print("작성자: ", author) 

print("작성 수: ", author_num) #1
print("가격: " , price) #2
print("텍스트 길이: " , length) #3
print("이미지 개수: " , img) #4
print("방문 수: ", attend_num) #5
print("직거래 여부: ", deliver) #6
print("카톡 여부: ", talk) #7
print("스팸 여부: ", spam)

data=[list(x) for x in zip(*temp_data)] 
print(data)

with open('airpodpro.csv', 'w', newline='') as file:
    writer=csv.writer(file)
    writer.writerow(['title', 'written_time', 'author', 'author_num', 'price', 'length', 'img', 'attend_num', 'deliver', 'talk', 'spam'])
    writer.writerows(data)


f = open('data.csv', 'w', newline="")
writing = csv.writer(f)
writing.writerow(title)
writing.writerow(author_num)
writing.writerow(written_time)

# %%
