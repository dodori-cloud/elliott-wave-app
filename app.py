import streamlit as st
import yfinance as yf
import pandas as pd
import time

# 1. UI 설정
st.set_page_config(layout="wide")
st.title("🚀 데이터 찌꺼기 완벽 제거 스캐너")

# 2. 캐싱 로직 (데이터 요청 차단 원천 봉쇄)
@st.cache_data(ttl=3600)
def get_stock_data(ticker):
    time.sleep(2.5) # 요청 간격 충분히 확보
    df = yf.download(ticker, period="1y", interval="1mo", auto_adjust=True, progress=False)
    return df

tickers = ['MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'AMD']

# 3. 메인 분석 엔진
if st.button("최종 정밀 스캔 시작"):
    data = []
    # 데이터 처리 상황 가시화
    with st.spinner('기관 수급 데이터 분석 중... (약 20초 소요)'):
        for ticker in tickers:
            try:
                df = get_stock_data(ticker)
                
                if not df.empty and 'Volume' in df.columns:
                    # VWAP 산출
                    vwap = float((df['Volume'] * ((df['High'] + df['Low'] + df['Close']) / 3)).sum() / df['Volume'].sum())
                    price = float(df['Close'].iloc[-1])
                    deviation = ((price - vwap) / vwap) * 100
                    
                    # 거래량 추세 분석
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
                continue # 특정 종목 실패 시 건너뛰고 계속 진행
    
    # 4. 결과 출력
    if data:
        st.table(pd.DataFrame(data))
    else:
        st.error("데이터를 불러올 수 없습니다. 잠시 후 다시 시도하세요.")

# 5. 가이드
st.write("---")
st.write("### 🚦 매매 판단 기준")
st.write("* **강력 매수신호:** 괴리율 10% 미만 + 거래량 증가")
st.write("* **보유 유지:** 괴리율 10% ~ 30%")
st.write("* **매도 고려:** 괴리율 30% 초과")
