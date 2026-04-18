import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(layout="wide")
st.title("📈 데이터 확인용 분석기")

ticker = st.text_input("티커 입력", "TSLA")

if st.button("데이터 분석 실행"):
    with st.spinner('데이터를 로딩 중입니다...'):
        try:
            # 1. 데이터 로드 확인
            df = yf.download(ticker, period="1y", interval="1wk", progress=False)
            
            if df.empty:
                st.error("데이터를 가져올 수 없습니다. 티커를 확인하세요.")
            else:
                # 2. 데이터가 보이면 성공
                st.success(f"{ticker} 데이터 {len(df)}개 로드 성공!")
                
                # 3. 차트 대신 표로 데이터 출력
                st.dataframe(df.tail(10), use_container_width=True)
                
                # 4. 변곡점 조건 계산
                df['pct'] = df['Close'].pct_change()
                peaks = df[df['pct'].abs() > 0.04]
                
                st.subheader("변곡점 리스트")
                st.table(peaks[['Close', 'pct']].tail(5))
        
        except Exception as e:
            st.error(f"예상치 못한 에러: {e}")
