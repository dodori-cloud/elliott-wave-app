import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(layout="wide")
st.title("🚀 최종 완성형 수급 & VWAP 스캐너")

@st.cache_data(ttl=3600)
def get_stock_data(ticker):
    time.sleep(3) 
    stock = yf.Ticker(ticker)
    df = stock.history(period="1y", interval="1mo")
    return df

tickers = ['MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'AMD']

if st.button("최종 통합 스캔 시작"):
    results = []
    for ticker in tickers:
        df = get_stock_data(ticker)
        if not df.empty and 'Volume' in df.columns:
            # 1. VWAP 계산 (거래량 가중 평균)
            typical_price = (df['High'] + df['Low'] + df['Close']) / 3
            vwap = (typical_price * df['Volume']).sum() / df['Volume'].sum()
            
            # 2. 괴리율 및 거래량 배수
            curr_price = df['Close'].iloc[-1]
            deviation = ((curr_price - vwap) / vwap) * 100
            vol_ratio = df['Volume'].iloc[-1] / df['Volume'].mean()
            
            # 3. 전략 적용 (괴리율 5% 이내 + 거래량 증가 시 매집)
            status = "🚀 매집중" if deviation < 5 and vol_ratio > 1.0 else "보유"
            
            results.append({
                '종목': ticker,
                '기관평단(VWAP)': f"${vwap:.2f}",
                '괴리율': f"{deviation:.1f}%",
                '거래량배수': f"{vol_ratio:.2f}배",
                '상태': status
            })
    
    st.table(pd.DataFrame(results))
