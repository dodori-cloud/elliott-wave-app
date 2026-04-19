import streamlit as st
import yfinance as yf
import pandas as pd

# 페이지 설정
st.set_page_config(layout="wide")
st.title("🚀 데이터 찌꺼기 완벽 제거 스캐너")

# 캐싱 적용: 24시간(86400초) 동안 데이터를 메모리에 보관하여 반복 요청 차단 방지
@st.cache_data(ttl=86400)
def get_stock_data(ticker):
    df = yf.download(ticker, period="1y", interval="1mo", auto_adjust=True, progress=False)
    return df

tickers = ['MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'AMD']

if st.button("최종 정밀 스캔 시작"):
    data = []
    for ticker in tickers:
        try:
            df = get_stock_data(ticker)
            
            if not df.empty and 'Volume' in df.columns:
                # VWAP 계산
                vwap = float((df['Volume'] * ((df['High'] + df['Low'] + df['Close']) / 3)).sum() / df['Volume'].sum())
                price = float(df['Close'].iloc[-1])
                
                # 괴리율 계산
                deviation = ((price - vwap) / vwap) * 100
                
                # 거래량 추세 (최근 3개월 평균 vs 전체 기간 평균)
                recent_vol = df['Volume'].tail(3).mean()
                avg_vol = df['Volume'].mean()
                vol_score = "📈 증가" if recent_vol > avg_vol else "📉 감소"
                
                # 최종 등급 로직
                if deviation < 10 and vol_score == "📈 증가":
                    status = "🚀 강력 매수신호"
                elif deviation > 30:
                    status = "⚠️ 매도 고려(과열)"
                else:
                    status = "✅ 보유 유지"
                
                data.append({
                    '종목': ticker,
                    '현재가': f"{price:,.2f}",
                    '기관평단': f"{vwap:,.2f}",
                    '괴리율': f"{deviation:.1f}%",
                    '거래량추세': vol_score,
                    '최종등급': status
                })
        except Exception as e:
            continue
    
    if data:
        st.table(pd.DataFrame(data))
    else:
        st.error("데이터를 가져오는 중 오류가 발생했거나 종목 데이터가 없습니다.")

# 투자 전략 가이드
st.write("---")
st.write("### 🚦 매매 판단 기준")
st.write("* **강력 매수신호:** 괴리율 10% 미만 + 거래량 증가 (기관 매집)")
st.write("* **보유 유지:** 괴리율 10% ~ 30%")
st.write("* **매도 고려:** 괴리율 30% 초과 (과열)")
