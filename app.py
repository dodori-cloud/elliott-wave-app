import streamlit as st
import yfinance as yf
import pandas as pd
import os

st.title("엘리어트 파동 자동 분석기")

# 데이터 캐싱 디렉토리 설정
DATA_FILE = "stock_data.csv"

@st.cache_data(ttl=3600) # 1시간 동안 데이터를 유지
def get_data(ticker):
    # 파일이 있으면 불러오고, 없으면 새로 다운로드
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE, index_col=0, parse_dates=True)
    else:
        df = yf.download(ticker, period="1y", interval="1d", progress=False)
        df.to_csv(DATA_FILE)
    return df

ticker = st.text_input("티커 입력 (예: TSLA, AAPL)", "TSLA")

if ticker:
    with st.spinner('데이터를 분석 중입니다...'):
        df = get_data(ticker)
        
        if not df.empty:
            # 차트 출력
            st.subheader(f"{ticker} 종가 차트")
            st.line_chart(df['Close'])
            
            # 파동 계산 로직
            sensitivity = st.slider("파동 민감도 조절", 0.01, 0.10, 0.03)
            df['diff'] = df['Close'].pct_change()
            df['Wave'] = df['diff'].abs() > sensitivity
            
            # 결과 표시
            st.write(f"감지된 변곡점: {df['Wave'].sum()}개")
            st.dataframe(df[df['Wave'] == True][['Close']])
        else:
            st.error("데이터 로드에 실패했습니다. 다시 시도해주세요.")
