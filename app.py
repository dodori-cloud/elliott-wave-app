import streamlit as st
import yfinance as yf
import pandas as pd

st.title("엘리어트 파동 자동 분석기")

@st.cache_data
def load_data(ticker):
    # 연결 안정성을 위해 설정을 최적화합니다.
    df = yf.download(ticker, period="2y", interval="1d", auto_adjust=True, threads=True)
    return df

ticker = st.text_input("티커 입력 (예: TSLA, AAPL)", "TSLA")

if ticker:
    with st.spinner(f'{ticker} 데이터를 불러오는 중...'):
        df = load_data(ticker)
        
        # 데이터 유효성 검사 (yfinance 데이터가 들어왔는지 확인)
        if not df.empty:
            # 1. 차트 그리기
            st.subheader(f"{ticker} 종가 차트")
            st.line_chart(df['Close'])
            
            # 2. 파동 계산 로직
            sensitivity = st.slider("파동 민감도 조절", 0.01, 0.10, 0.03)
            df['diff'] = df['Close'].pct_change()
            df['Wave'] = df['diff'].abs() > sensitivity
            
            # 3. 결과 출력
            st.write(f"감지된 변곡점: {df['Wave'].sum()}개")
            st.dataframe(df[df['Wave'] == True][['Close']])
            
        else:
            # 데이터가 비어있을 경우의 처리
            st.error("데이터를 불러오지 못했습니다. 티커명을 다시 확인해주세요.")
