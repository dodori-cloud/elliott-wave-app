import streamlit as st
import yfinance as yf
import pandas as pd

st.title("🚀 자동 종목 발굴 스캐너")

# 1. 대상 리스트를 코드에 미리 정의
tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'AMD'] 

if st.button("전체 종목 자동 스캔 시작"):
    results = []
    # 2. 루프를 돌며 모든 종목을 자동 분석
    for ticker in tickers:
        try:
            df_m = yf.download(ticker, period="3y", interval="1mo", progress=False)
            df_d = yf.download(ticker, period="3y", interval="1d", progress=False)
            
            vwap = (df_m['Volume'] * ((df_m['High'] + df_m['Low'] + df_m['Close']) / 3)).sum() / df_m['Volume'].sum()
            current_price = df_d['Close'].iloc[-1]
            
            # 필터링 조건: 매물대 중심(VWAP) 위에 있는 종목만!
            if current_price > vwap:
                results.append({'Ticker': ticker, 'Price': current_price, 'VWAP': vwap})
        except:
            continue
            
    # 3. 필터링된 결과만 자동 출력
    if results:
        st.dataframe(pd.DataFrame(results))
    else:
        st.write("조건에 맞는 종목이 없습니다.")
