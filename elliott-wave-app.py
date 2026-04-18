import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta

st.title("엘리어트 파동 자동 분석기")

# 1. 데이터 로드 함수
@st.cache_data
def load_data(ticker):
    df = yf.download(ticker, period="1y", interval="1d")
    return df

ticker = st.text_input("티커 입력 (예: TSLA, AAPL)", "TSLA")
df = load_data(ticker)

# 2. 기초적인 변곡점 찾기 (ZigZag 로직)
# pct를 조정하여 파동의 민감도를 조절합니다
def get_zigzag(df, pct=0.05):
    # 간단한 구현: 고점/저점 식별
    df['ZigZag'] = df['Close'].pct_change().abs() > pct
    return df

df = get_zigzag(df)

# 3. 차트 출력
st.line_chart(df['Close'])
st.write("분석된 데이터 상단:", df.tail())
