import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(layout="wide")
st.title("📈 주봉 변곡점 분석기 (최종 복구 버전)")

ticker = st.text_input("티커 입력 (예: TSLA)", "TSLA")

if ticker:
    # 1. 데이터 로드 후 인덱스 강제 재설정 (핵심)
    df = yf.download(ticker, period="3y", interval="1wk", auto_adjust=True, progress=False)
    df.reset_index(inplace=True) 
    
    if not df.empty:
        # 2. 변곡점 계산
        sensitivity = st.slider("민감도", 0.01, 0.10, 0.04)
        df['pct'] = df['Close'].pct_change()
        df['Wave'] = df['pct'].abs() > sensitivity
        peaks = df[df['Wave'] == True]

        # 3. 차트 생성
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], name='종가', line=dict(color='white')))
        fig.add_trace(go.Scatter(x=peaks['Date'], y=peaks['Close'], mode='markers', name='변곡점', marker=dict(color='red', size=8)))
        
        # 4. 차트 레이아웃 강제 설정
        fig.update_layout(height=600, template="plotly_dark", autosize=True)
        
        st.plotly_chart(fig, use_container_width=True)
        st.success(f"변곡점 {len(peaks)}개 탐지 완료")
