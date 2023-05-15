import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.express as px

# '/app/streamlit-practice/data/holidays_events.csv'
train = pd.read_parquet('data/train.parquet', engine = 'pyarrow')
holiday = pd.read_csv('data/holidays_events.csv')
transactions = pd.read_csv('data/transactions.csv')
stores = pd.read_csv('data/stores.csv')
oil = pd.read_csv('data/oil.csv')

##############################################################################
train['year'] = pd.to_datetime(train['date']).dt.year
train['month'] = pd.to_datetime(train['date']).dt.strftime("%B")
train['day_of_week'] = pd.to_datetime(train['date']).dt.day_name()

df_year_s = train.groupby('year')['sales'].mean()
df_year_s = df_year_s.reset_index()
df_year_s['color'] =['#e2e9d2', '#cbd1bd', '#b4baa8', '#9ea393', '#878b7e']

df_month_s = train.groupby('month')['sales'].mean()
df_month_s = df_month_s.sort_values('sales', ascending=True)
df_month_s['color'] = ['#ece8f4','#d9d2e9','#c3bdd1','#ada8ba','#9793a3','#827e8b','#6c6974','#56545d','#413f45','#2b2a2e','#151517','#000000']
new_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
df_month_s = df_month_s.reindex(new_order, axis=0)
df_month_s = df_month_s.reset_index()


df_day_of_week_s = train.groupby('day_of_week')['sales'].mean()
df_day_of_week_s = df_day_of_week_s.sort_values('sales', ascending=False)
df_day_of_week_s['color'] = ['rgb(255, 0, 0)','rgb(255, 36, 36)','rgb(255, 71, 71)','rgb(255, 107, 107)','rgb(255, 143, 143)','rgb(255, 179, 179)','rgb(255, 214, 214)']
new_order_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
df_day_of_week_s = df_day_of_week_s.reindex(new_order_week, axis=0)
df_day_of_week_s = df_day_of_week_s.reset_index()

df_year = train.groupby('year')['onpromotion'].mean()
df_year = df_year.reset_index()
df_year['color'] =['#e2e9d2', '#cbd1bd', '#b4baa8', '#9ea393', '#878b7e']

df_month = train.groupby('month')['onpromotion'].mean()
df_month = df_month.sort_values('onpromotion', ascending=True)
df_month['color'] = ['#ece8f4','#d9d2e9','#c3bdd1','#ada8ba','#9793a3','#827e8b','#6c6974','#56545d','#413f45','#2b2a2e','#151517','#000000']
new_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
df_month = df_month.reindex(new_order, axis=0)
df_month = df_month.reset_index()


df_day_of_week = train.groupby('day_of_week')['onpromotion'].mean()
df_day_of_week = df_day_of_week.sort_values('onpromotion', ascending=False)
df_day_of_week['color'] = ['rgb(255, 0, 0)','rgb(255, 36, 36)','rgb(255, 71, 71)','rgb(255, 107, 107)','rgb(255, 143, 143)','rgb(255, 179, 179)','rgb(255, 214, 214)']
new_order_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
df_day_of_week = df_day_of_week.reindex(new_order_week, axis=0)
df_day_of_week = df_day_of_week.reset_index()

fig = make_subplots(rows=3, cols=2, 
                    subplot_titles=("연도별 평균 Sales", "연도별 평균 Promotion", "월별 평균 Sales",
                                   "월별 평균 Promotion", "요일별 평균 Sales", "요일별 평균 Promotion"))
#SALES 
fig.append_trace(go.Bar(x=df_year_s['year'], y=df_year_s['sales'], marker = {'color': list(df_year_s['color'])}),
                row=1, col=1)


fig.append_trace(go.Bar(x=df_month_s['month'], y=df_month_s['sales'], marker = {'color': list(df_month_s['color'])}), 
                 row=2, col=1)

fig.append_trace(go.Bar(x=df_day_of_week_s['day_of_week'], y=df_day_of_week_s['sales'], marker = {'color': list(df_day_of_week_s['color'])}), row=3, col=1)

##ONPROMOTION
fig.append_trace(go.Bar(x=df_year['year'], y=df_year['onpromotion'], marker = {'color': list(df_year['color'])}),
                row=1, col=2)


fig.append_trace(go.Bar(x=df_month['month'], y=df_month['onpromotion'], marker = {'color': list(df_month['color'])}), 
                 row=2, col=2)

fig.append_trace(go.Bar(x=df_day_of_week['day_of_week'], y=df_day_of_week['onpromotion'],
                        marker = {'color': list(df_day_of_week['color'])}), row=3, col=2)
#styling
#fig.update_yaxes(showgrid=False, ticksuffix=' ', categoryorder='total ascending', row=1, col=1)
#fig.update_xaxes(visible=False, row=1, col=1)

fig.update_layout(height=1000, width=1400, title_text="SALES & ONPROMOTION ANALYSIS",  
                  title_font=dict(size=30, color='#783f04'), showlegend=False)
st.plotly_chart(fig)