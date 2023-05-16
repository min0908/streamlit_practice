import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from matplotlib.animation import FuncAnimation
import matplotlib.dates as mdates
import mplfinance as mpf

train = pd.read_parquet('data/train.parquet', engine = 'pyarrow')

store_nbr = st.number_input("상점 번호를 입력하세요", min_value=1)

if store_nbr:
    top5_sales = train[train['store_nbr'] == store_nbr].groupby('family')['sales'].sum().nlargest(5).reset_index()

    plt.figure(figsize=(10, 6))
    sns.barplot(x='family', y='sales', data=top5_sales, palette='viridis')
    plt.title(f'Store {store_nbr}: Top 5 selling product families')
    st.pyplot(plt)

st.write("")
st.subheader('**강진전후 애니메이션(sales)**')

train['date'] = pd.to_datetime(train['date'])

earthquake_date = pd.to_datetime('2016-04-16')

before_earthquake = train[train['date'] < earthquake_date]
after_earthquake = train[train['date'] >= earthquake_date]

before_earthquake_sales = before_earthquake.groupby('date')['sales'].sum().reset_index()
after_earthquake_sales = after_earthquake.groupby('date')['sales'].sum().reset_index()

fig, ax = plt.subplots()

dates = pd.date_range(start=before_earthquake_sales['date'].min(), end=after_earthquake_sales['date'].max(), freq='QS')

# 애니메이션을 위한 초기 그래프를 설정
line1, = ax.plot([], [], color='blue')
line2, = ax.plot([], [], color='red')

def animate(i):
    current_date = dates[i]
    if current_date < earthquake_date:
        data = before_earthquake_sales[before_earthquake_sales['date'] <= current_date]
        line1.set_data(data['date'], data['sales'])
    else:
        data = after_earthquake_sales[after_earthquake_sales['date'] <= current_date]
        line2.set_data(data['date'], data['sales'])

    ax.relim()
    ax.autoscale_view()
    ax.set_xlim(before_earthquake_sales['date'].min(), dates[i])  # x축 범위 업데이트
    ax.xaxis.set_major_locator(mdates.YearLocator())  # x축 눈금 설정
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))  # x축 눈금 형식 설정
    return line1, line2,

# 애니메이션을 생성
ani = FuncAnimation(fig, animate, frames=len(dates), blit=True)
ani.save('animation.gif', writer='pillow')

# Display the animation in Streamlit
st.image('animation.gif', use_container_width=True)
