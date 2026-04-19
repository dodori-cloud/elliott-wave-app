import streamlit as st
import yfinance as yf
import pandas as pd
import time

# 1. 페이지 및 UI 설정
st.set_page_config(page_title="기관 수급 스캐너", layout="wide")
st.title("🚀 데이터 찌꺼기 완벽 제거 스캐너")

# 2. 캐싱 및 데이터 로직 (야후 파이낸스 차단 방지)
@st.cache_data(ttl=3600)
def get_stock_data(ticker):
    time.sleep(2.5) # 요청 간격 충분히 확보
    df = yf.download(ticker, period="1y", interval="1mo", auto_adjust=True, progress=False)
    return df

tickers = ['MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'AMD']

# 3. 메인 분석 프로세스
if st.button("최종 정밀 스캔 시작"):
    data = []
    status_text = st.empty()
    
    with st.spinner('기관 수급 데이터 분석 중...'):
        for ticker in tickers:
            status_text.text(f"분석 중: {ticker}...")
            try:
                df = get_stock_data(ticker)
                
                if not df.empty and 'Volume' in df.columns:
                    # VWAP 산출
                    vwap = float((df['Volume'] * ((df['High'] + df['Low'] + df['Close']) / 3)).sum() / df['Volume'].sum())
                    price = float(df['Close'].iloc[-1])
                    deviation = ((price - vwap) / vwap) * 100
                    
                    # 거래량 추세
                    recent_vol = df['Volume'].tail(3).mean()
                    avg_vol = df['Volume'].mean()
                    vol_score = "📈 증가" if recent_vol > avg_vol else "📉 감소"
                    
                    # 등급 산정
                    status = "🚀 강력 매수신호" if deviation < 10 and vol_score == "📈 증가" else ("⚠️ 매도 고려(과열)" if deviation > 30 else "✅ 보유 유지")
                    
                    data.append({
                        '종목': ticker, 
                        '현재가': f"{price:,.2f}", 
                        '기관평단': f"{vwap:,.2f}", 
                        '괴리율': f"{deviation:.1f}%", 
                        '거래량추세': vol_score, 
                        '최종등급': status
                    })
            except Exception:
                continue
    
    status_text.empty()
    
    # 4. 결과 출력 (데이터가 있으면 무조건 출력)
    if data:
        st.table(pd.DataFrame(data))
    else:
        st.error("데이터를 불러오지 못했습니다. 종목 리스트나 네트워크를 확인하세요.")

# 5. 가이드
st.write("---")
st.write("### 🚦 매매 판단 기준")
st.write("* **강력 매수신호:** 괴리율 10% 미만 + 거래량 증가")
st.write("* **보유 유지:** 괴리율 10% ~ 30%")
st.write("* **매도 고려:** 괴리율 30% 초과")
