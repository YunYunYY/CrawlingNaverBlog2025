# CrawlingNaverBlog2025
- 제주 아라동 맛집 정보를 간략하게 확인해보자.
- 어떤 아라동 맛집이 인기일까?
- 블로거들은 리뷰를 작성할 때 어떤 키워드를 주로 사용하나?

### project_crawling.py
1. 네이버 API 이용 -> 네이버 블로그 검색 상위 포스팅의 제목, 링크 수집
2. 수집한 링크를 돌며 각 포스팅의 내용, 해시태그, 장소, 주소 수집
3. 제목 및 내용 정제
4. 수집한 정보를 "sns_posts.csv"로 저장

### project_nlp.py
1. 크롤링으로 얻은 포스팅 내용 분석 ->"sns_posts.csv"
2. konlpy를 이용하여 명사, 형용사 분석
3. pyplot과 wordcloud를 이용하여 시각화

### project_map.py
1. 네이버 API 이용 -> 장소의 위도 및 경도 수집
2. 분류가 음식점이 아닌 장소 필터
3. 맵을 통해 시각화. 언급된 수가 많을수록 지도에 표시된 원이 크다.

---
#### 사용한 API
https://developers.naver.com/docs/serviceapi/search/local/local.md#%EC%A7%80%EC%97%AD
https://developers.naver.com/docs/serviceapi/search/blog/blog.md#%EB%B8%94%EB%A1%9C%EA%B7%B8
