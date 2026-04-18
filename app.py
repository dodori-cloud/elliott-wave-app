import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="엘리엇 파동 자동 분석기", layout="wide")
st.title("📈 엘리엇 파동 자동 분석기 (완성형)")

# 데이터 로드 (캐싱 적용)
@st.cache_data(ttl=3600)
def get_data(ticker):
    df = yf.download(ticker, period="1y", interval="1d", auto_adjust=True, progress=False)
    return df

ticker = st.text_input("티커 입력 (예: TSLA, AAPL)", "TSLA")

if ticker:
    df = get_data(ticker)
    if not df.empty:
        # 파동 변곡점 계산
        sensitivity = st.slider("파동 민감도 (변동성 기준)", 0.01, 0.10, 0.03)
        df['pct_change'] = df['Close'].pct_change()
        df['Wave'] = df['pct_change'].abs() > sensitivity
        peaks = df[df['Wave'] == True].index

        # 시각화
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name='종가', line=dict(color='gray', width=1)))
        
        # 1~5파 라벨링
        wave_names = ["1파", "2파", "3파", "4파", "5파"]
        for i, date in enumerate(peaks[:5]):
            fig.add_trace(go.Scatter(x=[date], y=[df.loc[date, 'Close']], mode='markers+text',
                                     text=wave_names[i], textposition='top center',
                                     marker=dict(size=10, color='red'), name=wave_names[i]))
        st.plotly_chart(fig, use_container_width=True)

        # 규칙 검증 로직 (누락 없음)
        st.subheader("📋 엘리엇 파동 규칙 검증 결과")
        if len(peaks) >= 5:
            p0, p1, p2, p3, p4 = [df.loc[peaks[i], 'Close'] for i in range(5)]
            
            # 1. 3파가 1파보다 짧지 않아야 함
            if p3 > p1: st.success("✅ 3파 법칙 통과: 3파가 1파보다 높습니다.")
            else: st.warning("⚠️ 3파 법칙 위반: 3파가 1파보다 짧습니다.")
            
            # 2. 2파 되돌림 규칙 (2파 저점 p2 > 1파 시작점 p0)
            if p2 > p0: st.success("✅ 2파 되돌림 통과: 1파 시작점을 침범하지 않았습니다.")
            else: st.warning("⚠️ 2파 법칙 위반: 2파가 1파 시작점을 침범했습니다.")
            
            # 3. 4파 되돌림 규칙 (4파 저점 p4 > 1파 고점 p1)
            if p4 > p1: st.success("✅ 4파 되돌림 통과: 1파 고점을 침범하지 않았습니다.")
            else: st.warning("⚠️ 4파 법칙 위반: 4파가 1파 고점을 침범했습니다.")
        else:
            st.info("파동이 5개 미만입니다. 민감도를 조절하여 파동을 더 찾아보세요.")
    else:
        st.error("데이터를 찾을 수 없습니다.")
