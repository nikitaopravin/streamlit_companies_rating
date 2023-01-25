import yfinance as yf
import streamlit as st
import pandas as pd
import datetime

st.header('''Это приложение показывает котировки компании Apple, Google, Amazon за указанный период 
          *вы можете настроить отображение используя меню слева''')

st.sidebar.header('Настройки')
ticker_choosen = st.sidebar.radio('компания', ('Apple', 'Google', 'Amazon'), index=0)
ticker = {'Apple': 'AAPL', 'Google': 'GOOGL', 'Amazon': 'AMZN'}
start_date = st.sidebar.date_input('начало периода', datetime.date(2010, 1, 1))
end_date = st.sidebar.date_input('конец периода', datetime.date(2020, 1, 1))

ticker_data = yf.Ticker(ticker[ticker_choosen])
ticker_df = ticker_data.history(period='1D', start=start_date, end=end_date)


st.subheader('Стоимость акций')
st.line_chart(ticker_df['Close'])
st.subheader('Рынчная капитализация')
st.area_chart(ticker_df['Volume'])

with st.expander('Cырые данные'):
    ticker_df
