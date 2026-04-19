import streamlit as st
import yfinance as yf
import pandas as pd

def calculate_clean_vwap(ticker):
    # 월봉 데이터로 VWAP 계산
    df = yf.download(ticker, period="3y", interval="1mo", progress=False)
    # 데이터가 비어있지 않은지 확인
    if df.empty: return None
    
    # 순수 숫자 값만 추출 (텍스트 제거)
    volume = df['Volume'].astype(float)
    price = ((df['High'] + df['Low'] + df['Close']) / 3).astype(float)
    
    vwap = (price * volume).sum() / volume.sum()
    current_price = yf.Ticker(ticker).history(period="1d")['Close'].iloc[-1]
    
    return current_price, vwap

# 결과 출력 로직
if st.button("정밀 스캔 시작"):
    ticker = 'NVDA' # 예시
    price, vwap = calculate_clean_vwap(ticker)
    deviation = ((price - vwap) / vwap) * 100
    
    st.write(f"현재가: {price:.2f}")
    st.write(f"정밀 VWAP: {vwap:.2f}")
    st.write(f"순수 괴리율: {deviation:.2f}%")
