import streamlit as st
import yfinance as yf
import pandas as pd

st.title("엘리어트 파동 자동 분석기")

@st.cache_data(ttl=3600)
def get_data(ticker):
    # auto_adjust=True를 사용하여 복잡한 MultiIndex 구조를 단순화합니다.
    df = yf.download(ticker, period="1y", interval="1d", auto_adjust=True, progress=False)
    return df

ticker = st.text_input("티커 입력 (예: TSLA, AAPL)", "TSLA")

if ticker:
    with st.spinner('데이터 분석 중...'):
        df = get_data(ticker)
        
        # 데이터가 비어있는지 먼저 확인
        if df.empty:
            st.error("데이터를 불러올 수 없습니다. 티커명을 확인하거나 잠시 후 다시 시도하세요.")
        else:
            # 데이터프레임의 구조가 단순한지 확인
            if 'Close' in df.columns:
                st.line_chart(df['Close'])
                
                # 파동 분석
                sensitivity = st.slider("파동 민감도", 0.01, 0.10, 0.03)
                df['diff'] = df['Close'].pct_change()
                df['Wave'] = df['diff'].abs() > sensitivity
                
                st.write(f"감지된 변곡점: {df['Wave'].sum()}개")
                st.dataframe(df[df['Wave'] == True][['Close']])
            else:
                st.write("데이터 구조가 예상과 다릅니다. 현재 데이터 컬럼:", df.columns.tolist())
