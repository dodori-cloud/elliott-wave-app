import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(layout="wide")
st.title("🚀 자동 종목 발굴 스캐너")

tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'AMD']

if st.button("전체 종목 자동 스캔 시작"):
    results = []
    for ticker in tickers:
        try:
            df_m = yf.download(ticker, period="3y", interval="1mo", progress=False)
            df_d = yf.download(ticker, period="3y", interval="1d", progress=False)
            
            if not df_m.empty and not df_d.empty:
                vwap = (df_m['Volume'] * ((df_m['High'] + df_m['Low'] + df_m['Close']) / 3)).sum() / df_m['Volume'].sum()
                current_price = df_d['Close'].iloc[-1]
                
                # 모든 종목을 결과에 추가 (테스트를 위해 조건 완화)
                results.append({'Ticker': ticker, 'Price': round(current_price, 2), 'VWAP': round(vwap, 2)})
        except:
            continue
            
    if results:
        st.dataframe(pd.DataFrame(results), use_container_width=True)
    else:
        st.write("분석된 종목이 없습니다.")
