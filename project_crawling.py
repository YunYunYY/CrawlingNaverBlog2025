import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import urllib.request
import json

def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


# 네이버 검색 API 예제 - 블로그 검색
client_id = "client_id"
client_secret = "client_secret"
encText = urllib.parse.quote("제주 아라동 맛집") #검색어
url = "https://openapi.naver.com/v1/search/blog?query=" + encText # JSON 결과

#몇 개?
display=20
url+="&display="+str(display)

request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)
response = urllib.request.urlopen(request)
rescode = response.getcode()

if(rescode==200):
    response_body = response.read()
    json_response = response_body.decode('utf-8')
    json_response=json.loads(json_response)
    # print(json_response['items'][0]['title'])
    
    titles=[]
    links=[]

    for i in range(display):
        titles.append(remove_html_tags(json_response['items'][i]['title']).strip())
        links.append(json_response['items'][i]['link'])
    # print(titles)
    # print(links)

    #본문 내용 스크랩
    contents=[] #내용
    hashtags=[] #해시태그
    location=[] #장소이름
    address=[] #주소
    for i in range(display):
        url=links[i]
        driver = webdriver.Chrome()
        driver.get(url)
        time.sleep(1)

        driver._switch_to.frame('mainFrame')
        content=driver.find_element(By.CSS_SELECTOR,".se-main-container")
        # print(content.text)

        contents.append(remove_html_tags(content.text).strip())

        #해시태그 수집...
        hashtag=[]
        tag=driver.find_elements(By.CLASS_NAME, "wrap_tag")
        for i in tag:
            hashtag=i.text.strip().split("\n")
        txthashtag="".join(hashtag[1:])
        hashtags.append(txthashtag)

        #장소 수집
        try:
            map_pic=driver.find_element(By.CSS_SELECTOR,"a.se-map-info")
            map_json = map_pic.get_attribute("data-linkdata")
            map_json = map_json.replace("&quot;", '"')
            map_json=json.loads(map_json)
            print(map_json.get('placeId'))
            href_value="https://map.naver.com/v5/entry/place/"+map_json.get('placeId')
            driver.get(href_value)
            time.sleep(2)

            driver._switch_to.frame('entryIframe')

            location_name=driver.find_element(By.CSS_SELECTOR,".GHAhO")
            location_address=driver.find_element(By.CSS_SELECTOR,".LDgIH")
            print(location_name.text)
            print(location_address.text)
            location.append(location_name.text)
            address.append(location_address.text)

        except Exception :
            try:
                link_element = driver.find_element(By.CSS_SELECTOR, ".location a")
                href_value = link_element.get_attribute("href")
                print(href_value)
                driver.get(href_value)
                time.sleep(2)

                driver._switch_to.frame('entryIframe')

                location_name=driver.find_element(By.CSS_SELECTOR,".GHAhO")
                location_address=driver.find_element(By.CSS_SELECTOR,".LDgIH")
                print(location_name.text)
                print(location_address.text)
                location.append(location_name.text)
                address.append(location_address.text)
            except Exception:
                #지도 정보가 없는 것
                location.append('')
                address.append('')

        driver.quit()


    #내용 정제...
    df=pd.DataFrame({'titles':titles,'links':links,'location':location,'address':address,'hashtag':hashtags,'contents':contents})
    df['titles']=df['titles'].str.replace('[^가-힣A-Za-z0-9#\s]', '', regex=True)
    df['contents']= df['contents'].str.replace('\n', ' ', regex=True)
    df['contents']= df['contents'].str.replace('[^가-힣A-Za-z0-9#\s]', '', regex=True)
    
    # print(df['contents'][0])

    # #본문 해시태그 분리 > 필요한가??
    # hashtag=[]
    # for i in range(display):
    #     cc=df['contents'][i].split()
    #     h=[]
    #     for j in cc:
    #         if j.startswith('#'):
    #             print(j)
    #             h.append(j)
    #     hashtag.append(h)

    # print(df['hashtag'])
    df.to_csv("sns_posts.csv",encoding="utf-8-sig",index=False)


else:
    print("Error Code:" + rescode)


