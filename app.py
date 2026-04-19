import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(layout="wide")
st.title("🚀 데이터 검증 완료: 종목 발굴 스캐너")

tickers = ['MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'AMD']

if st.button("정밀 스캔 실행"):
    data = []
    for ticker in tickers:
        df_m = yf.download(ticker, period="3y", interval="1mo", progress=False)
        df_d = yf.download(ticker, period="1d", progress=False)
        
        if not df_m.empty and not df_d.empty:
            # VWAP 계산 (정밀하게)
            vwap = (df_m['Volume'] * ((df_m['High'] + df_m['Low'] + df_m['Close']) / 3)).sum() / df_m['Volume'].sum()
            price = float(df_d['Close'].iloc[-1])
            
            # 괴리율 계산 (%)
            deviation = ((price - vwap) / vwap) * 100
            
            data.append({
                'Ticker': ticker,
                'Price': round(price, 2),
                'VWAP': round(vwap, 2),
                'Deviation(%)': round(deviation, 2),
                'Status': '⚠️과열' if deviation > 40 else '✅양호'
            })
    
    df_results = pd.DataFrame(data)
    st.dataframe(df_results, use_container_width=True)
