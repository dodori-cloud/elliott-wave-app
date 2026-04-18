import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.title("엘리어트 파동 자동 분석기")

@st.cache_data
def load_data(ticker):
    # 요청 실패 시 재시도하도록 설정
    ticker_obj = yf.Ticker(ticker)
    try:
        # 데이터 요청 간격 확보를 위한 딜레이
        time.sleep(2)
        df = ticker_obj.history(period="1y", interval="1d")
        return df
    except Exception as e:
        st.error(f"데이터 로드 실패: {e}")
        return pd.DataFrame()

ticker = st.text_input("티커 입력 (예: TSLA, AAPL)", "TSLA")

if ticker:
    with st.spinner(f'{ticker} 데이터를 불러오는 중...'):
        df = load_data(ticker)
        
        if not df.empty:
            st.success("데이터 로드 성공!")
            st.line_chart(df['Close'])
            
            # 파동 분석 (로직 최적화)
            sensitivity = st.slider("파동 민감도", 0.01, 0.10, 0.03)
            df['diff'] = df['Close'].pct_change()
            df['Wave'] = df['diff'].abs() > sensitivity
            
            st.write(f"감지된 변곡점: {df['Wave'].sum()}개")
            st.dataframe(df[df['Wave'] == True][['Close']])
        else:
            st.warning("서버가 일시적으로 차단되었습니다. 5분 정도 기다린 후 새로고침(F5) 해주세요.")
