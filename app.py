import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(page_title="주봉 변곡점 분석기", layout="wide")
st.title("📈 주봉 변곡점 분석기 (3년 데이터)")

# 1. 3년치 주봉 데이터 로드
@st.cache_data(ttl=3600)
def get_data(ticker):
    return yf.download(ticker, period="3y", interval="1wk", auto_adjust=True, progress=False)

ticker = st.text_input("티커 입력 (예: TSLA, AAPL)", "TSLA")

if ticker:
    df = get_data(ticker)
    if not df.empty:
        # 2. 민감도 조절 (변곡점 탐색)
        sensitivity = st.slider("파동 민감도 (클수록 큰 파동 탐색)", 0.01, 0.10, 0.04)
        df['pct'] = df['Close'].pct_change()
        df['Wave'] = df['pct'].abs() > sensitivity
        peaks = df[df['Wave'] == True]

        # 3. 차트 시각화
        fig = go.Figure()
        # 기본 종가 차트
        fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name='종가', line=dict(color='gray', width=1)))
        
        # 변곡점 마커 표시
        fig.add_trace(go.Scatter(x=peaks.index, y=peaks['Close'], mode='markers', 
                                 marker=dict(color='red', size=8), name='변곡점'))
        
        st.plotly_chart(fig, use_container_width=True)
        st.write(f"총 {len(peaks)}개의 변곡점이 탐지되었습니다.")
    else:
        st.error("데이터를 불러올 수 없습니다. 티커를 확인하세요.")
