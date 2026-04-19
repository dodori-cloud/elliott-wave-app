import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(layout="wide")
st.title("🚀 데이터 100% 강제 추출 스캐너")

tickers = ['MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'AMD']

if st.button("전체 종목 강제 스캔 실행"):
    data = []
    for ticker in tickers:
        try:
            # 1. auto_adjust=True를 통해 수정주가(Split/Dividend 반영) 사용
            # 2. progress=False로 속도 최적화
            df = yf.download(ticker, period="3y", interval="1mo", auto_adjust=True, progress=False)
            
            # 데이터가 비어있지 않은지 더 엄격하게 체크
            if not df.empty and 'Volume' in df.columns:
                # 데이터 값만 정제 (Pandas Series 찌꺼기 제거)
                vwap = (df['Volume'] * ((df['High'] + df['Low'] + df['Close']) / 3)).sum() / df['Volume'].sum()
                
                # 마지막 종가 가져오기 (가장 최근 데이터)
                last_price = float(df['Close'].iloc[-1])
                vwap_val = float(vwap)
                
                deviation = ((last_price - vwap_val) / vwap_val) * 100
                
                data.append({
                    'Ticker': ticker,
                    'Price': f"{last_price:,.2f}",
                    'VWAP': f"{vwap_val:,.2f}",
                    'Deviation(%)': f"{deviation:,.2f}%",
                    'Status': '⚠️과열' if deviation > 40 else '✅양호'
                })
            else:
                st.write(f"⚠️ {ticker}: 데이터 형식 오류 혹은 거래량 데이터 부재")
        except Exception as e:
            st.write(f"❌ {ticker}: 데이터 로드 중 예상치 못한 에러 - {e}")
    
    if data:
        st.table(pd.DataFrame(data))
