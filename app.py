import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time

st.title("엘리어트 파동 자동 분석기")

@st.cache_data(ttl=3600)
def get_data(ticker):
    df = yf.download(ticker, period="1y", interval="1d", progress=False)
    # yfinance 버전 대응
    if isinstance(df.columns, pd.MultiIndex):
        df = df.xs(ticker, axis=1, level=0)
    return df

ticker = st.text_input("티커 입력 (예: TSLA, AAPL)", "TSLA")

if ticker:
    df = get_data(ticker)
    if not df.empty:
        # 파동 민감도 슬라이더
        sensitivity = st.slider("파동 민감도 조절", 0.01, 0.10, 0.03)
        df['diff'] = df['Close'].pct_change()
        df['Wave'] = df['diff'].abs() > sensitivity
        
        # 1. 변곡점 시각화 (Plotly)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name='종가', line=dict(color='gray', width=1)))
        
        # 변곡점만 점으로 표시
        waves = df[df['Wave'] == True]
        fig.add_trace(go.Scatter(x=waves.index, y=waves['Close'], mode='markers', name='변곡점', 
                                 marker=dict(color='red', size=8)))
        
        st.plotly_chart(fig)
        
        # 2. 파동 라벨링 준비 (데이터프레임)
        st.subheader("감지된 변곡점 리스트")
        st.dataframe(waves[['Close']])
    else:
        st.error("데이터를 찾을 수 없습니다.")
