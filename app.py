import streamlit as st
import yfinance as yf
import pandas as pd
import re

# 숫자만 추출하는 함수
def extract_number(value):
    s = str(value)
    # 문자열에서 숫자와 소수점만 남기고 다 제거
    clean = re.sub(r'[^0-9.]', '', s)
    return float(clean) if clean else 0.0

st.set_page_config(layout="wide")
st.title("🚀 데이터 찌꺼기 완벽 제거 스캐너")

tickers = ['MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'AMD']

if st.button("최종 정밀 스캔 시작"):
    data = []
    for ticker in tickers:
        try:
            df = yf.download(ticker, period="5y", interval="1mo", progress=False)
            if not df.empty and 'Volume' in df.columns:
                vwap = (df['Volume'] * ((df['High'] + df['Low'] + df['Close']) / 3)).sum() / df['Volume'].sum()
                price = df['Close'].iloc[-1]
                
                # 찌꺼기 제거 함수 적용
                vwap_val = extract_number(vwap)
                price_val = extract_number(price)
                
                deviation = ((price_val - vwap_val) / vwap_val) * 100
                
                data.append({
                    'Ticker': ticker,
                    'Price': f"{price_val:,.2f}",
                    'VWAP': f"{vwap_val:,.2f}",
                    'Deviation(%)': f"{deviation:,.2f}%"
                })
        except: continue
    
    if data:
        st.table(pd.DataFrame(data))
