import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="엘리엇 파동 자동 분석기", layout="wide")
st.title("📈 엘리엇 파동 자동 분석기 (최종 완성형)")

@st.cache_data(ttl=3600)
def get_data(ticker):
    return yf.download(ticker, period="3y", interval="1wk", auto_adjust=True, progress=False)

ticker = st.text_input("티커 입력 (예: TSLA, MSFT)", "TSLA")

if ticker:
    df = get_data(ticker)
    if not df.empty and len(df) > 50:
        sensitivity = st.slider("파동 민감도", 0.01, 0.10, 0.04)
        df['pct'] = df['Close'].pct_change()
        df['Wave'] = df['pct'].abs() > sensitivity
        peaks = df[df['Wave'] == True].index

        # 시각화
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name='종가', line=dict(color='gray')))
        
        labels = ["1파", "2파", "3파", "4파", "5파", "A파", "B파", "C파"]
        
        if len(peaks) > 0:
            for i, date in enumerate(peaks):
                label = labels[i % 8]
                fig.add_trace(go.Scatter(x=[date], y=[df.loc[date, 'Close']], 
                                         mode='markers+text', text=label, textposition='top center',
                                         marker=dict(size=8, color='red'), name=label))
            
            # 현재 상태 출력
            curr_idx = (len(peaks) - 1) % 8
            st.write(f"### 현재 위치: **{labels[curr_idx]}**")
            
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("데이터 부족: 티커를 확인하세요.")
