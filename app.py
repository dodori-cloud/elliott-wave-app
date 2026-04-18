import streamlit as st
import yfinance as yf
import pandas as pd

st.title("엘리어트 파동 자동 분석기")

# 데이터 로드
@st.cache_data
def load_data(ticker):
    df = yf.download(ticker, period="1y", interval="1d", auto_adjust=True)
    return df

ticker = st.text_input("티커 입력 (예: TSLA, AAPL)", "TSLA")

if ticker:
    df = load_data(ticker)
    
    # [핵심 로직] pandas_ta 없이 직접 파동 찾기 (ZigZag 로직)
    # 종가 기준 5% 이상 변동 시 변곡점으로 판단
    def detect_waves(df, pct=0.05):
        df['diff'] = df['Close'].pct_change()
        df['Wave'] = df['diff'].abs() > pct
        return df

    df = detect_waves(df)
    
    st.subheader(f"{ticker} 차트 및 변곡점")
    st.line_chart(df['Close'])
    
    # 변곡점만 필터링하여 표시
    waves = df[df['Wave'] == True]
    st.write("감지된 변곡점:", waves[['Close']])
