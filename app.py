import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(layout="wide")
st.title("🚀 유망 종목 스크리닝 엔진 (월봉 기준)")

# 대상 종목 리스트 (간소화하여 실행 확인 후 확장하세요)
tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA']

@st.cache_data(ttl=3600)
def get_stock_metrics(ticker):
    try:
        stock = yf.Ticker(ticker)
        # 월봉, 주봉, 일봉 데이터 로드 (3년)
        df_m = yf.download(ticker, period="3y", interval="1mo", progress=False)
        df_w = yf.download(ticker, period="3y", interval="1wk", progress=False)
        df_d = yf.download(ticker, period="3y", interval="1d", progress=False)
        
        if df_m.empty or df_w.empty or df_d.empty: return None

        # 1. 매물대 중심 (VWAP)
        vwap = (df_m['Volume'] * ((df_m['High'] + df_m['Low'] + df_m['Close']) / 3)).sum() / df_m['Volume'].sum()
        
        # 2. 40주 이평선 (주봉)
        ma40_w = df_w['Close'].rolling(window=40).mean().iloc[-1]
        
        # 3. RSI
        def get_rsi(df, period=14):
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            rs = gain / loss
            return 100 - (100 / (1 + rs.iloc[-1]))

        return {
            'Ticker': ticker,
            'Price': df_d['Close'].iloc[-1],
            'VWAP': vwap,
            'Above_VWAP': df_d['Close'].iloc[-1] > vwap,
            'Above_MA40W': df_w['Close'].iloc[-1] > ma40_w,
            'RSI_D': get_rsi(df_d),
            'RSI_W': get_rsi(df_w)
        }
    except:
        return None

if st.button("종목 스크리닝 시작"):
    with st.spinner('종목 데이터를 분석 중입니다...'):
        data = [get_stock_metrics(t) for t in tickers]
        df_final = pd.DataFrame([d for d in data if d is not None])
        
        # 필터링 조건 (매물대 중심 위에 있는 종목만)
        filtered_df = df_final[df_final['Above_VWAP'] == True]
        
        st.subheader("✅ 필터링된 유망 종목 리스트")
        st.dataframe(filtered_df, use_container_width=True)
