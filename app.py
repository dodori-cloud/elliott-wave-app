import streamlit as st
import yfinance as yf
import pandas as pd

st.title("엘리어트 파동 자동 분석기")

@st.cache_data
def load_data(ticker):
    # period를 늘려 더 많은 데이터를 가져옵니다.
    df = yf.download(ticker, period="2y", interval="1d", auto_adjust=True)
    return df

ticker = st.text_input("티커 입력 (예: TSLA, AAPL)", "TSLA")

if ticker:
    df = load_data(ticker)
    
    # [민감도 조절 슬라이더] 0.01(1%) ~ 0.1(10%) 사이 조절
    sensitivity = st.slider("파동 민감도 조절 (변동폭 %)", 0.01, 0.10, 0.03)
    
    def detect_waves(df, pct):
        df['diff'] = df['Close'].pct_change()
        # 절대값으로 파동의 방향과 무관하게 변동폭을 체크
        df['Wave'] = df['diff'].abs() > pct
        return df

    df = detect_waves(df, sensitivity)
    
    st.subheader(f"{ticker} 차트 및 변곡점")
    st.line_chart(df['Close'])
    
    # 변곡점만 필터링
    waves = df[df['Wave'] == True]
    st.write(f"현재 민감도 {sensitivity*100}% 기준 감지된 변곡점 수: {len(waves)}")
    st.dataframe(waves[['Close']])
