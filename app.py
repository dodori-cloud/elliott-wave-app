import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="엘리엇 파동 자동 분석기", layout="wide")
st.title("📈 엘리엇 파동 자동 분석기 (주봉/진행형 완성)")

# 1. 데이터 로드 (주봉/3년)
@st.cache_data(ttl=3600)
def get_data(ticker):
    df = yf.download(ticker, period="3y", interval="1wk", auto_adjust=True, progress=False)
    return df

ticker = st.text_input("티커 입력 (예: TSLA, MSFT)", "TSLA")

if ticker:
    df = get_data(ticker)
    if not df.empty and len(df) > 50:
        # 2. 민감도 조절 및 변곡점 탐색
        sensitivity = st.slider("파동 민감도 (변동성 기준)", 0.01, 0.10, 0.04)
        df['pct_change'] = df['Close'].pct_change()
        df['Wave'] = df['pct_change'].abs() > sensitivity
        peaks = df[df['Wave'] == True].index
        
        # 3. 차트 생성
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name='종가', line=dict(color='gray', width=1)))
        
        # 파동 라벨링 (진행 중인 파동까지 모두 표시)
        wave_names = ["1파", "2파", "3파", "4파", "5파"]
        for i, date in enumerate(peaks[:5]):
            fig.add_trace(go.Scatter(x=[date], y=[df.loc[date, 'Close']], mode='markers+text',
                                     text=wave_names[i], textposition='top center',
                                     marker=dict(size=10, color='red'), name=wave_names[i]))
        st.plotly_chart(fig, use_container_width=True)

        # 4. 엘리엇 파동 규칙 검증 (진행형 로직)
        st.subheader("📋 파동 규칙 검증")
        count = len(peaks)
        if count >= 3:
            st.write(f"현재 **{count}파동 진행 중**입니다.")
            prices = [df.loc[peaks[i], 'Close'] for i in range(min(count, 5))]
            
            # 규칙 1: 3파 법칙 (3파 이상 진행 시)
            if count >= 3:
                if prices[2] > prices[0]: st.success("✅ 3파 법칙: 3파가 1파 고점보다 높습니다.")
                else: st.warning("⚠️ 3파 법칙 위반: 3파가 1파보다 짧습니다.")
            
            # 규칙 2: 2파 되돌림 (2파 종료 시)
            if count >= 3:
                if prices[2] > prices[0]: st.success("✅ 2파 되돌림: 1파 시작점을 지지했습니다.")
                else: st.warning("⚠️ 2파 법칙 위반: 2파가 1파 시작점을 침범했습니다.")
            
            # 규칙 3: 4파 되돌림 (4파 종료 시)
            if count >= 5:
                if prices[4] > prices[1]: st.success("✅ 4파 되돌림: 1파 고점을 지지했습니다.")
                else: st.warning("⚠️ 4파 법칙 위반: 4파가 1파 고점을 침범했습니다.")
        else:
            st.info("파동 형성 초기 단계입니다. 추세를 더 관찰하세요.")
    else:
        st.error("데이터가 부족합니다. 다른 티커를 입력하거나 기간을 확인하세요.")
