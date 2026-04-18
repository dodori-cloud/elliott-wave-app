import streamlit as st
import yfinance as yf
import pandas as pd

st.title("엘리어트 파동 자동 분석기")

@st.cache_data
def load_data(ticker):
    # 데이터를 2년치로 넉넉하게 가져옵니다
    df = yf.download(ticker, period="2y", interval="1d", auto_adjust=True)
    return df

ticker = st.text_input("티커 입력 (예: TSLA, AAPL)", "TSLA")

if ticker:
    df = load_data(ticker)
    
    # [중요] 데이터가 제대로 로드되었는지 확인
    if df.empty:
        st.error("데이터를 불러오지 못했습니다. 티커명을 확인하세요.")
    else:
        st.write(f"{ticker} 데이터 {len(df)}개 로드 완료")
        
        sensitivity = st.slider("파동 민감도 조절", 0.01, 0.10, 0.03)
        
        df['diff'] = df['Close'].pct_change()
        df['Wave'] = df['diff'].abs() > sensitivity
        
        # 차트 출력 전에 데이터가 있는지 확인
        if not df['Close'].empty:
            st.subheader(f"{ticker} 종가 차트")
            st.line_chart(df['Close'])
            
            waves = df[df['Wave'] == True]
            st.write(f"감지된 변곡점: {len(waves)}개")
            st.dataframe(waves[['Close']])
        else:
            st.warning("차트를 그릴 데이터가 없습니다.")
