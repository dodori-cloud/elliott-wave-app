import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

# 페이지 설정 (전체 화면 활용)
st.set_page_config(page_title="주봉 분석기", layout="wide")
st.title("📈 주봉 변곡점 분석기")

@st.cache_data(ttl=3600)
def get_data(ticker):
    # 데이터를 로드하고 결측치를 제거합니다.
    df = yf.download(ticker, period="3y", interval="1wk", auto_adjust=True, progress=False)
    return df.dropna()

ticker = st.text_input("티커 입력 (예: TSLA)", "TSLA")

if ticker:
    with st.spinner('데이터 분석 중...'):
        df = get_data(ticker)
        
        if not df.empty:
            sensitivity = st.slider("민감도 (변동성 기준)", 0.01, 0.10, 0.04)
            df['pct'] = df['Close'].pct_change()
            df['Wave'] = df['pct'].abs() > sensitivity
            peaks = df[df['Wave'] == True]

            # 컨테이너를 사용하여 차트 영역 강제 확보
            with st.container():
                fig = go.Figure()
                
                # 라인 차트
                fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name='종가', 
                                         line=dict(color='#00CC96', width=2)))
                
                # 변곡점 마커
                if not peaks.empty:
                    fig.add_trace(go.Scatter(x=peaks.index, y=peaks['Close'], mode='markers', 
                                             marker=dict(color='red', size=8), name='변곡점'))
                
                # 레이아웃 강제 수정
                fig.update_layout(
                    template="plotly_dark",
                    margin=dict(l=20, r=20, t=30, b=20),
                    height=500,
                    xaxis=dict(showgrid=True, title="날짜"),
                    yaxis=dict(showgrid=True, title="가격")
                )
                
                # 차트 출력
                st.plotly_chart(fig, use_container_width=True)
                
            st.success(f"총 {len(peaks)}개의 변곡점이 탐지되었습니다.")
        else:
            st.error("데이터가 비어있습니다. 티커를 확인해주세요.")
