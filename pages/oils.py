import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.express as px

# '/app/streamlit-practice/data/holidays_events.csv'
train = pd.read_parquet('data/train.parquet', engine = 'pyarrow')
oil = pd.read_csv('data/oil.csv')

oil.loc[oil['date'] == '2013-01-01', 'dcoilwtico'] = 93.14
oil = oil.interpolate(method='linear', limit=20) #보간법




tab1, tab2 = st.tabs(["**일자별 비교(by date)**", "**산점도**"])

with tab1:
    train_aux = train[['date', 'sales', 'onpromotion']].groupby('date').mean()
    train_aux = train_aux.reset_index()

    fig = make_subplots(rows=2, cols=1, 
                    subplot_titles=("평균 sales", "Oil Price"))
    fig.append_trace(go.Scatter(x=train_aux['date'], y=train_aux['sales'],marker_color='#b4a7d6', text="sales"), row=1, col=1)
    fig.append_trace(go.Scatter(x=oil['date'], y=oil['dcoilwtico'],marker_color='blue', text="sales"), row=2, col=1)

    fig.update_layout(height=1000, width=1400, title_text="SALES & OIL ANALYSIS BY DATE",  
                    title_font=dict(size=30, color='#783f04'), showlegend=False)
    
    st.plotly_chart(fig, use_container_width=True)


train['date'] = pd.to_datetime(train['date'])
oil['date'] = pd.to_datetime(oil['date'])

train['sales'] = pd.to_numeric(train['sales'], errors='coerce')
train = train.dropna(subset=['sales'])

sales_oil = train.groupby('date').mean()['sales']
sales_oil = sales_oil.reset_index()

sales_oil = pd.merge(sales_oil, oil, on ='date', how='left')


with tab2:
    fig3 = px.scatter(sales_oil, x="dcoilwtico", y="sales", size='sales', color='sales',
                  color_continuous_scale="fall")

    # fig3.update_layout(title={'text': '프로모션은 평균 sales에 영향을 미칠까?'},showlegend=False , width="100%")
    st.plotly_chart(fig3, use_container_width=True)  