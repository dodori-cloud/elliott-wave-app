import streamlit as st
import yfinance as yf
import pandas as pd
import time # 간격 조절용

st.set_page_config(layout="wide")
st.title("🚀 데이터 찌꺼기 완벽 제거 스캐너")

@st.cache_data(ttl=86400)
def get_stock_data(ticker):
    # 요청마다 짧은 대기시간을 강제로 부여
    time.sleep(1.2) 
    df = yf.download(ticker, period="1y", interval="1mo", auto_adjust=True, progress=False)
    return df

tickers = ['MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'AMD']

if st.button("최종 정밀 스캔 시작"):
    data = []
    # 에러가 나면 전체가 멈추지 않게 개별 처리
    progress_bar = st.progress(0)
    for i, ticker in enumerate(tickers):
        try:
            df = get_stock_data(ticker)
            
            if not df.empty and 'Volume' in df.columns:
                vwap = float((df['Volume'] * ((df['High'] + df['Low'] + df['Close']) / 3)).sum() / df['Volume'].sum())
                price = float(df['Close'].iloc[-1])
                deviation = ((price - vwap) / vwap) * 100
                
                recent_vol = df['Volume'].tail(3).mean()
                avg_vol = df['Volume'].mean()
                vol_score = "📈 증가" if recent_vol > avg_vol else "📉 감소"
                
                status = "🚀 강력 매수신호" if deviation < 10 and vol_score == "📈 증가" else ("⚠️ 매도 고려(과열)" if deviation > 30 else "✅ 보유 유지")
                
                data.append({'종목': ticker, '현재가': f"{price:,.2f}", '기관평단': f"{vwap:,.2f}", '괴리율': f"{deviation:.1f}%", '거래량추세': vol_score, '최종등급': status})
        except Exception:
            continue
        progress_bar.progress((i + 1) / len(tickers))
    
    if data:
        st.table(pd.DataFrame(data))
    else:
        st.error("잠시 후 다시 시도해주세요. (서버 제한 초과)")
