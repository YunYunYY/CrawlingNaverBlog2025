import folium
import pandas as pd
import json
import requests
import os
import sys
import urllib.request
from collections import Counter

csv_open=pd.read_csv('sns_posts.csv',usecols=[2,3])

csv_open=csv_open.dropna()
location=csv_open['location']
address=csv_open['address']

x=[]
y=[]


# 네이버 검색 API 예제 - 블로그 검색
client_id = "client_id"
client_secret = "client_secret"


for i in location:
    encText = urllib.parse.quote(i) #검색어
    url = "https://openapi.naver.com/v1/search/local?query=" + encText # JSON 결과

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()

    if(rescode==200):
        response_body = response.read()
        json_response = response_body.decode('utf-8')
        json_response=json.loads(json_response)

        x.append(int(json_response['items'][0]['mapx'])/10000000)
        y.append(int(json_response['items'][0]['mapy'])/10000000)

print(x)
print(y)

csv_open['x']=x
csv_open['y']=y

#counting
z=Counter(location)


map_ara = folium.Map(location=[y[0],x[0]],zoom_start=13)
for i,j,k in zip(x,y,location):
    folium.Marker([float(j),float(i)],tooltip=k,popup=f"count:{z.get(k)}").add_to(map_ara)
    folium.CircleMarker([float(j),float(i)],radius = z.get(k) * 30,fill_color='skyblue').add_to(map_ara)

map_ara.save('hotplace_map.html')


