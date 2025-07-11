from konlpy.tag import Okt
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from wordcloud import WordCloud

okt = Okt()

csv_open=pd.read_csv('sns_posts.csv')

contest_list=csv_open['contents']
okt_list=[]
kk_noun=[]
kk_abjective=[]


#일단 명사, 형용사만 분리해서 넣어둠.
for i in contest_list:
    okt_list=okt.pos(i,norm=True,stem=True)
    kk_noun.extend(i for i, j in okt_list if j in ['Noun'] and i not in['수', '곳','것','제주','아라동','제주시','맛집'])
    kk_abjective.extend(i for i, j in okt_list if j in ['Adjective']and i not in['이다','스럽다'])
    

#막대 그래프
fpath = "C:/Windows/Fonts/MALGUNSL.ttf"
font_name = fm.FontProperties(fname=fpath).get_name()
plt.rc('font', family=font_name)
plt.figure(figsize=(12, 7))
plt.xlabel("명사")
plt.ylabel("빈도")
xn=[]
yn=[]

for i,j in Counter(kk_noun).most_common(20):
    xn.append(i)
    yn.append(j)
plt.bar(xn,yn)
plt.xticks(rotation=45)
for i, v in enumerate(yn):
    plt.text(i, v, str(v),ha='center',va='bottom')
plt.savefig("pyplot_noun.png")
plt.show()


plt.figure(figsize=(12, 7))
plt.xlabel("형용사")
plt.ylabel("빈도")
xa=[]
ya=[]

for i,j in Counter(kk_abjective).most_common(20):
    xa.append(i)
    ya.append(j)
plt.bar(xa,ya)
for i, v in enumerate(ya):
    plt.text(i, v, str(v),ha='center',va='bottom')
plt.xticks(rotation=45)
plt.savefig("pyplot_abjective.png")
plt.show()


#WordCloud
# wc = WordCloud(width = 1000, height = 600, background_color="white", font_path=font_path, max_words=20).generate_from_frequencies(Counter(kk_abjective))
# plt.imshow(wc.generate_from_frequencies(Counter(kk_abjective)))

wc = WordCloud(font_path=fpath,background_color='white', width=800, height=400,colormap='seismic_r',max_words=100).generate_from_frequencies(Counter(kk_noun))
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.savefig("WordCloud_noun.png")
plt.show()

wc = WordCloud(font_path=fpath,background_color='white', width=800, height=400,colormap='CMRmap',max_words=100).generate_from_frequencies(Counter(kk_abjective))
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.savefig("WordCloud_abjective.png")
plt.show()