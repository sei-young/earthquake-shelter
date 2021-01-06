#!/usr/bin/env python
# coding: utf-8

# # 라이브러리 불러오기

# In[1]:


import sys
import requests
import json
import pandas as pd
import numpy as np
from pandas.io.json import json_normalize
import os
import webbrowser
import folium
from folium import plugins
print(folium.__version__)


# # 파일 불러오기

# In[2]:


df = pd.read_csv("C:/Users/user/Desktop/빅데이터프로젝트1/나이100상건물_위도경도.csv", encoding='euc-kr')


# In[3]:


df.info()


# In[4]:


data = pd.read_csv('C:/Users/user/Desktop/빅데이터프로젝트1/지반침하정보_20180903.csv',encoding = 'utf-8')


# In[5]:


data.info()


# In[6]:


data2 = pd.read_csv('C:/Users/user/Desktop/빅데이터프로젝트1/2018-20200923국내지진목록.csv',encoding = 'utf-8')


# In[7]:


data2.head(1)


# In[8]:


EarthquakeOutdoorsShelter_df = pd.read_csv("C:/Users/user/Desktop/빅데이터프로젝트1/EarthquakeOutdoorsShelter_df_sejong.csv", encoding='euc-kr')


# In[9]:


EarthquakeOutdoorsShelter_df.info()


# In[10]:


#세종시 경계 위도,경도
state_geo = 'C:/Users/user/Desktop/빅데이터프로젝트1/sejong3.json'


# In[11]:


#세종시 읍면동별 지역코드와 인구수
state_unemployment = 'C:/Users/user/Desktop/빅데이터프로젝트1/읍면동별 세대 및 인구2.csv'
state_data = pd.read_csv(state_unemployment, encoding = 'euc-kr')
state_data.columns = ['CODE', 'POPULATION']
state_data['CODE'] = state_data.CODE.map(lambda x : str(x).zfill(7))


# In[12]:


state_data


# # 데이터 전처리

# In[13]:


data2['도시'] = data2['위치'].str.split(" ").str[0]
data2['위도'] = data2['위도'].str.split(" ").str[0]
data2['경도'] = data2['경도'].str.split(" ").str[0]

location = data2[(data2['도시'] == '충남') | (data2['도시'] == '충북')]


# # 지도 그리기

# In[14]:


#기본 위치
mymap = folium.Map(location=[36.532176,127.274796], zoom_start=12)

#각layer별로 카테고리 나누기
fg_4 = folium.FeatureGroup(name = '옥외대피소').add_to(mymap)
fg_1 = folium.FeatureGroup(name = '100년 이상 된 건물').add_to(mymap)
fg_2 = folium.FeatureGroup(name = '지반침하사고').add_to(mymap)
fg_3 = folium.FeatureGroup(name = '지진').add_to(mymap)


# In[15]:


#내 위치 표시하기
plugins.LocateControl(auto_start=True, strings = {"title":"현재 위치보기","popup":"내 위치"}, flyTo = True,drawCircle = True).add_to(mymap)


# In[16]:


#옥외 대피소 표시하기
for i in EarthquakeOutdoorsShelter_df.index:
  folium.Marker([EarthquakeOutdoorsShelter_df['위도'][i], EarthquakeOutdoorsShelter_df['경도'][i]], tooltip=EarthquakeOutdoorsShelter_df['시설명'][i]).add_to(fg_4)


# In[17]:


#지반 침하사고 표시하기
for i in data.index:
    folium.Marker([data['위도'][i], data['경도'][i]],icon=folium.Icon(color='red',icon='star'),popup=folium.Popup(data['최초발생원인'][i],max_width=450),tooltip=data['지반침하지역상세'][i]).add_to(fg_2)


# In[18]:


#지진 표시하기
for i in location.index:
    folium.CircleMarker([location['위도'][i], location['경도'][i]], popup = folium.Popup(location['발생시각'][i],max_width=450),tooltip=location['위치'][i], radius = (location['규모'][i])**5 , color = '#ffffgg', fill_color='#fffggg').add_to(fg_3)


# In[19]:


#100년 이상 된 건물 표시하기
from folium.plugins import MarkerCluster
marker_cluster = MarkerCluster().add_to(fg_1)

for i in df.index:
  folium.Marker(location = [df['위도'][i], df['경도'][i]], popup=folium.Popup(df['주소'][i],max_width=450), icon=folium.Icon(color='green',icon='ok')).add_to(marker_cluster)


# In[20]:


#위치 찍으면 직선거리 알려줌
#plugins.MeasureControl( position = 'topright' , primary_length_unit = 'meters' , secondary_length_unit = 'miles' , primary_area_unit = 'sqmeters' , secondary_area_unit = 'acres' ).add_to(mymap)


# In[22]:


#layerGroup([marker1, marker2]).addLayer(polyline).addTo(mymap);


# In[23]:


#인구 밀도 표시하기
mymap.choropleth(
    geo_data=state_geo,
    name='인구밀도',
    data=state_data,
    columns=['CODE', 'POPULATION'],
    key_on='feature.properties.code',
    fill_color='PuBu',
    fill_opacity=0.7,
    line_opacity=0.3,
    color = 'gray',
    legend_name = 'Population'
)

folium.LayerControl().add_to(mymap)


# In[24]:


#지도
mymap


# In[25]:


#저장하기
mymap.save('세종_건물_대피소_인구밀도.html')
a=folium.Map().get_root().render()


# In[ ]:




