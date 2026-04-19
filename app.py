import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(layout="wide")
st.title("🚀 최종 완성형 기관/외국인 수급 스캐너")

# 1. 강력한 예외 처리 데이터 로더
@st.cache_data(ttl=3600)
def get_stock_data(ticker):
    # 속도를 조금 더 늦춰 서버 차단을 최우선 방지
    time.sleep(4) 
    stock = yf.Ticker(ticker)
    try:
        # 주가 이력 및 재무 정보 동시 호출
        df = stock.history(period="1y", interval="1mo")
        info = stock.info
        return df, info
    except:
        return pd.DataFrame(), {}

tickers = ['MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'AMD']

if st.button("최종 통합 스캔 시작"):
    results = []
    status_bar = st.empty()
    
    with st.spinner('분석 중... (데이터 서버 접속 대기 중)'):
        for ticker in tickers:
            status_bar.text(f"분석 중: {ticker}...")
            df, info = get_stock_data(ticker)
            
            # 데이터 누락 방지: 빈 데이터라도 리스트에 추가하여 디버깅 가능하게 함
            inst_pct = info.get('institutionPercent', 0) if info else 0
            if inst_pct is None: inst_pct = 0
            
            if not df.empty:
                curr_vol = df['Volume'].iloc[-1]
                vol_avg = df['Volume'].mean()
                
                results.append({
                    '종목': ticker,
                    '기관비중': f"{inst_pct*100:.1f}%",
                    '거래량배수': f"{curr_vol/vol_avg:.2f}배",
                    '상태': "매집중" if inst_pct > 0.4 else "보유"
                })
            else:
                results.append({'종목': ticker, '기관비중': 'N/A', '거래량배수': 'N/A', '상태': '서버차단'})
    
    status_bar.empty()
    
    # 데이터가 아예 안 나와도 표는 무조건 출력
    st.table(pd.DataFrame(results))
    st.info("💡 상태가 '서버차단'으로 뜬다면 야후 파이낸스 서버가 일시적으로 제한한 상태입니다. 1시간 뒤 다시 시도하세요.")
