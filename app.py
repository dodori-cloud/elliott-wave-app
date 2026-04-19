import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(layout="wide")
st.title("🚀 기관/외국인 수급 & 기술적 분석 스캐너")

# 1. 기술적 분석 지표 (RSI)
def calculate_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

# 2. 데이터 가져오기 (캐싱)
@st.cache_data(ttl=3600)
def get_stock_data(ticker):
    time.sleep(3) # 서버 차단 방지
    stock = yf.Ticker(ticker)
    df = stock.history(period="1y", interval="1mo")
    return df, stock

tickers = ['MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'AMD']

if st.button("최종 통합 스캔 시작"):
    results = []
    with st.spinner('기관 수급 및 기술 지표 분석 중...'):
        for ticker in tickers:
            try:
                df, stock = get_stock_data(ticker)
                if not df.empty:
                    # [기술 지표] RSI 및 거래량 분석
                    df['RSI'] = calculate_rsi(df)
                    recent_rsi = df['RSI'].iloc[-1]
                    vol_avg = df['Volume'].mean()
                    curr_vol = df['Volume'].iloc[-1]
                    
                    # [수급 대리 지표] 기관/외국인 데이터 (재무 정보 활용)
                    # 야후 파이낸스는 institutionPercent 정보를 제공함
                    info = stock.info
                    inst_pct = info.get('institutionPercent', 0) * 100
                    
                    results.append({
                        '종목': ticker,
                        '기관보유비율': f"{inst_pct:.1f}%",
                        '현재RSI': f"{recent_rsi:.1f}",
                        '거래량대비': f"{curr_vol/vol_avg:.2f}배",
                        '상태': "매집중" if inst_pct > 50 and recent_rsi < 60 else "관망"
                    })
            except: continue
    
    st.table(pd.DataFrame(results))
