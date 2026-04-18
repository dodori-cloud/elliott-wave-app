import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

# 1. 페이지 설정 (넓은 레이아웃 강제)
st.set_page_config(page_title="주봉 분석기", layout="wide")
st.title("📈 주봉 변곡점 분석기")

@st.cache_data(ttl=3600)
def get_data(ticker):
    df = yf.download(ticker, period="3y", interval="1wk", auto_adjust=True, progress=False)
    # 데이터가 비어있지 않도록 정제
    return df.dropna()

ticker = st.text_input("티커 입력 (예: TSLA)", "TSLA")

if ticker:
    df = get_data(ticker)
    
    if not df.empty:
        # 민감도 슬라이더
        sensitivity = st.slider("파동 민감도", 0.01, 0.10, 0.04)
        df['pct'] = df['Close'].pct_change()
        df['Wave'] = df['pct'].abs() > sensitivity
        peaks = df[df['Wave'] == True]

        # 2. 차트 객체 생성 (가로세로 비율 최적화)
        fig = go.Figure()
        
        # 주가 라인
        fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name='종가', 
                                 line=dict(color='#00CC96', width=2)))
        
        # 변곡점 (마커)
        if not peaks.empty:
            fig.add_trace(go.Scatter(x=peaks.index, y=peaks['Close'], mode='markers', 
                                     marker=dict(color='red', size=8), name='변곡점'))
        
        # 3. 레이아웃 강제 설정 (X축/Y축 표시 보장)
        fig.update_layout(
            autosize=True,
            height=500, # 고정 높이 설정
            margin=dict(l=50, r=50, t=50, b=50),
            xaxis=dict(showgrid=True, zeroline=False, title="날짜"),
            yaxis=dict(showgrid=True, zeroline=False, title="가격"),
            template="plotly_dark"
        )
        
        # 4. 차트 출력
        st.plotly_chart(fig, use_container_width=True)
        st.success(f"총 {len(peaks)}개의 변곡점이 탐지되었습니다.")
    else:
        st.error("데이터를 불러올 수 없습니다.")
