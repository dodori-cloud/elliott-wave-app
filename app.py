import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.title("엘리어트 파동 자동 분석기")

# 데이터를 가져오는 함수
@st.cache_data
def load_data(ticker):
    # 타임아웃을 피하기 위해 1초 대기
    time.sleep(1)
    # 데이터를 1년치만 확실하게 불러오기
    df = yf.download(ticker, period="1y", interval="1d", progress=False)
    return df

ticker = st.text_input("티커 입력 (예: TSLA, AAPL)", "TSLA")

if ticker:
    with st.spinner(f'{ticker} 데이터를 불러오는 중...'):
        df = load_data(ticker)
        
        # 1. 데이터가 비어있는지 먼저 확인
        if df.empty:
            st.error("데이터를 가져올 수 없습니다. 서버 제한 상태일 수 있습니다.")
        else:
            # 2. 데이터 구조 보정 (yfinance 버전별 대응)
            if isinstance(df.columns, pd.MultiIndex):
                df = df.xs(ticker, axis=1, level=0)
            
            # 3. 차트 출력 전 데이터 확인
            if 'Close' in df.columns:
                st.subheader(f"{ticker} 종가 차트")
                # 인덱스 정렬 확인
                df = df.sort_index()
                st.line_chart(df['Close'])
                
                # 4. 파동 분석 로직
                sensitivity = st.slider("파동 민감도 조절", 0.01, 0.10, 0.03)
                df['diff'] = df['Close'].pct_change()
                df['Wave'] = df['diff'].abs() > sensitivity
                
                st.write(f"감지된 변곡점: {df['Wave'].sum()}개")
                st.dataframe(df[df['Wave'] == True][['Close']])
            else:
                st.error("종가(Close) 데이터를 찾을 수 없습니다.")
