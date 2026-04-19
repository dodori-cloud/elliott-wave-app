import streamlit as st
import yfinance as yf
import pandas as pd
import re

def extract_number(value):
    s = str(value)
    clean = re.sub(r'[^0-9.]', '', s)
    return float(clean) if clean else 0.0

tickers = ['MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'AMD']

if st.button("기관 수급 점수 스캔"):
    data = []
    for ticker in tickers:
        try:
            # 1년치 월봉 데이터로 분석
            df = yf.download(ticker, period="1y", interval="1mo", progress=False)
            if not df.empty and 'Volume' in df.columns:
                # VWAP 및 가격 추출
                vwap = (df['Volume'] * ((df['High'] + df['Low'] + df['Close']) / 3)).sum() / df['Volume'].sum()
                price = df['Close'].iloc[-1]
                
                v_val = extract_number(vwap)
                p_val = extract_number(price)
                
                # 핵심 분석 로직
                deviation = ((p_val - v_val) / v_val) * 100
                
                # 거래량 가중치 분석 (최근 3개월 거래량이 평균보다 높은가?)
                recent_vol = df['Volume'].tail(3).mean()
                avg_vol = df['Volume'].mean()
                vol_score = "📈 증가" if recent_vol > avg_vol else "📉 감소"
                
                # 등급 계산
                if deviation < 10 and vol_score == "📈 증가":
                    status = "🚀 강력 매수신호"
                elif deviation > 30:
                    status = "⚠️ 매도 고려(과열)"
                else:
                    status = "✅ 보유 유지"
                
                data.append({
                    '종목': ticker,
                    '현재가': f"{p_val:,.2f}",
                    '기관평단': f"{v_val:,.2f}",
                    '괴리율': f"{deviation:.1f}%",
                    '거래량추세': vol_score,
                    '최종등급': status
                })
        except: continue
    
    st.table(pd.DataFrame(data))
