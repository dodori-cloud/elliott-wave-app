import streamlit as st
import yfinance as yf
import pandas as pd
import time # 시간 지연을 위한 라이브러리 추가

st.title("엘리어트 파동 자동 분석기")

@st.cache_data
def load_data(ticker):
    # 데이터를 바로 가져오지 않고, 요청 시 간격을 둡니다.
    time.sleep(1) 
    # yfinance 설정을 좀 더 가볍게 조정합니다.
    df = yf.download(ticker, period="1y", interval="1d", progress=False)
    return df

ticker = st.text_input("티커 입력 (예: TSLA, AAPL)", "TSLA")

if ticker:
    # 1. 데이터 로드 전 확인
    df = load_data(ticker)
    
    # 2. 결과 처리
    if not df.empty:
        st.success(f"{ticker} 데이터 로드 성공!")
        st.line_chart(df['Close'])
        
        # 3. 파동 계산 (최소한의 로직으로)
        sensitivity = st.slider("민감도", 0.01, 0.10, 0.03)
        df['diff'] = df['Close'].pct_change()
        df['Wave'] = df['diff'].abs() > sensitivity
        
        st.dataframe(df[df['Wave'] == True][['Close']])
    else:
        st.error("서버 요청 제한(Rate Limit)에 걸렸습니다. 잠시(1~5분) 뒤에 다시 시도해주세요.")
