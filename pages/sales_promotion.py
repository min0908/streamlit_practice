import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.express as px


train = pd.read_parquet('/min0908/streamlit-practice/data/train.parquet', engine = 'pyarrow')

holiday = pd.read_csv('/min0908/streamlit-practice/data/holidays_events.csv')
transactions = pd.read_csv('/min0908/streamlit-practice/data/transactions.csv')
stores = pd.read_csv('/min0908/streamlit-practice/data/stores.csv')
oil = pd.read_csv('/min0908/streamlit_practice/data/train.parquet/streamlit-practice/data/oil.csv')

# 'holiday여부' 열 추가 및 초기값 0으로 설정
train['holiday여부'] = 0
# 'date'를 기준으로 holiday에 있는 날짜에 해당되는 행을 찾아 'holiday여부' 값을 1로 설정
train.loc[train['date'].isin(holiday['date']), 'holiday여부'] = 1

# 날짜 파생변수 생성
train['date'] = pd.to_datetime(train['date'])
train['day_of_week'] = train['date'].dt.dayofweek #요일
train['month'] = train['date'].dt.month #월
train['year'] = train['date'].dt.year #년도

# 날짜 인덱스로 설정
#train = train.set_index('date')
# id 컬럼 제거
train = train.drop('id',axis = 1)
# store_nbr, family는 카테고리로 만들기
train[['store_nbr', 'family']] = train[['store_nbr','family']].astype('category')

train_aux = train[['date', 'sales', 'onpromotion']].groupby('date').mean()
train_aux = train_aux.reset_index()

fig = make_subplots(rows=2, cols=1, 
                    subplot_titles=("일자별 평균 sales", "일자별 평균 Promotion"))
fig.append_trace(go.Scatter(x=train_aux['date'], y=train_aux['sales'],marker_color='#b4a7d6', text="sales"), row=1, col=1)
fig.append_trace(go.Scatter(x=train_aux['date'], y=train_aux['onpromotion'],marker_color='#93c47d', text="promotion"), row=2, col=1)

fig.update_layout(height=1000, width=1400, title_text="SALES & ONPROMOTION ANALYSIS",  
                  title_font=dict(size=30, color='#8a8d93'), showlegend=False)

st.plotly_chart(fig)