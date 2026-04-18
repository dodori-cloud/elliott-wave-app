import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="주봉 분석기", layout="wide")
st.title("📈 주봉 변곡점 분석기")

@st.cache_data(ttl=3600)
def get_data(ticker):
    # 데이터를 다운로드하고 결측치를 제거하여 완벽하게 정제합니다.
    df = yf.download(ticker, period="3y", interval="1wk", auto_adjust=True, progress=False)
    df = df.dropna()
    return df

ticker = st.text_input("티커 입력 (예: TSLA)", "TSLA")

if ticker:
    df = get_data(ticker)
    
    if not df.empty:
        # 변동성 기준으로 변곡점 탐지
        sensitivity = st.slider("민감도", 0.01, 0.10, 0.04)
        df['pct'] = df['Close'].pct_change()
        # NaN 값 처리: 첫 행은 pct_change가 NaN이므로 False 처리
        df['Wave'] = df['pct'].abs() > sensitivity
        
        # 변곡점만 필터링
        peaks = df[df['Wave'] == True]

        # 차트 그리기
        fig = go.Figure()
        
        # 1. 주가 라인 (명확하게 날짜 인덱스를 사용)
        fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name='종가', 
                                 line=dict(color='white', width=1)))
        
        # 2. 변곡점 마커 (데이터가 있을 때만)
        if not peaks.empty:
            fig.add_trace(go.Scatter(x=peaks.index, y=peaks['Close'], mode='markers', 
                                     marker=dict(color='red', size=8), name='변곡점'))
        
        # 레이아웃 강제 지정 (가장 중요한 부분)
        fig.update_layout(
            title=f"{ticker} 주봉 변곡점",
            xaxis_title="날짜",
            yaxis_title="가격",
            template="plotly_dark",
            height=600
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.success(f"총 {len(peaks)}개의 변곡점이 탐지되었습니다.")
    else:
        st.error("데이터를 불러올 수 없습니다. 티커명을 확인하세요.")
