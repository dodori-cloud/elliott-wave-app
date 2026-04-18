import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(page_title="주봉 변곡점 분석기", layout="wide")
st.title("📈 주봉 변곡점 분석기 (3년 데이터)")

@st.cache_data(ttl=3600)
def get_data(ticker):
    # 데이터를 좀 더 안정적으로 가져오기 위해 auto_adjust=True 설정
    df = yf.download(ticker, period="3y", interval="1wk", auto_adjust=True, progress=False)
    return df

ticker = st.text_input("티커 입력 (예: TSLA, AAPL)", "TSLA")

if ticker:
    with st.spinner('데이터를 불러오고 분석 중입니다...'):
        df = get_data(ticker)
        
        if not df.empty and len(df) > 10:
            sensitivity = st.slider("파동 민감도 (클수록 큰 파동)", 0.01, 0.10, 0.04)
            df['pct'] = df['Close'].pct_change()
            # 데이터의 절대값이 아닌 실제 종가 움직임을 기반으로 변곡점 판별
            df['Wave'] = df['pct'].abs() > sensitivity
            peaks = df[df['Wave'] == True]

            # 차트 설정
            fig = go.Figure()
            # 1. 주가 라인
            fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name='종가', 
                                     line=dict(color='#636EFA', width=2)))
            
            # 2. 변곡점 마커
            if not peaks.empty:
                fig.add_trace(go.Scatter(x=peaks.index, y=peaks['Close'], mode='markers', 
                                         marker=dict(color='#EF553B', size=10, symbol='circle'), 
                                         name='변곡점'))
            
            # 차트 레이아웃 최적화
            fig.update_layout(
                height=500,
                margin=dict(l=20, r=20, t=30, b=20),
                template="plotly_dark",
                hovermode="x unified"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.success(f"총 {len(peaks)}개의 변곡점이 탐지되었습니다.")
        else:
            st.warning("데이터가 너무 적거나 티커명이 잘못되었습니다.")
