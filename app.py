import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(layout="wide")
st.title("🚀 유망 종목 스크리닝 엔진 (월봉 기준)")

# 종목 리스트
tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA']

@st.cache_data(ttl=3600)
def get_stock_metrics(ticker):
    try:
        # 데이터 로드 (월봉/주봉/일봉)
        df_m = yf.download(ticker, period="3y", interval="1mo", progress=False)
        df_w = yf.download(ticker, period="3y", interval="1wk", progress=False)
        df_d = yf.download(ticker, period="3y", interval="1d", progress=False)
        
        if df_m.empty or df_d.empty: return None

        # 1. 매물대 중심 (VWAP)
        vwap = (df_m['Volume'] * ((df_m['High'] + df_m['Low'] + df_m['Close']) / 3)).sum() / df_m['Volume'].sum()
        
        # 2. 결과 딕셔너리 생성
        return {
            'Ticker': ticker,
            'Price': df_d['Close'].iloc[-1],
            'VWAP': vwap,
            'Above_VWAP': df_d['Close'].iloc[-1] > vwap
        }
    except:
        return None

if st.button("종목 스크리닝 시작"):
    with st.spinner('데이터를 수집하고 필터링 중입니다...'):
        # 데이터를 리스트로 수집 후 필터링
        raw_data = [get_stock_metrics(t) for t in tickers]
        clean_data = [d for d in raw_data if d is not None]
        
        if clean_data:
            df_final = pd.DataFrame(clean_data)
            # 안전하게 필터링
            filtered_df = df_final[df_final['Above_VWAP'] == True]
            
            st.subheader("✅ 필터링된 유망 종목 리스트")
            st.dataframe(filtered_df, use_container_width=True)
        else:
            st.error("분석 가능한 데이터를 가져오지 못했습니다.")
