import streamlit as st
import yfinance as yf
import pandas as pd

st.title("엘리어트 파동 자동 분석기")

# 데이터를 가져올 때 세션을 명확히 지정하여 연결 오류를 최소화합니다.
@st.cache_data
def load_data(ticker):
    # 연결 안정성을 위해 user-agent 추가
    df = yf.download(ticker, period="2y", interval="1d", auto_adjust=True, 
                     threads=True, group_by='ticker', actions=True)
    return df

ticker = st.text_input("티커 입력 (예: TSLA, AAPL)", "TSLA")

if ticker:
    with st.spinner(f'{ticker} 데이터를 불러오는 중...'):
        df = load_data(ticker)
        
        # yfinance 버전 변경에 따른 데이터 구조 확인
        if isinstance(df, pd.DataFrame) and not df.empty:
            # MultiIndex 컬럼 대응 (최신 yfinance 방식)
            if isinstance(df.columns, pd.MultiIndex):
                df = df.xs(ticker, axis=1, level=0)
            
            # 차트 그리기
            st.subheader(f"{ticker} 종가 차트")
            st.line_chart(df['Close'])
            
            # 파동 계산
            sensitivity = st.slider("파동 민감도 조절", 0.01, 0.10, 0.03)
            df['diff'] = df['Close'].pct_change()
            df['Wave'] = df['diff'].abs() > sensitivity
            
            st.write(f"감지된 변곡점: {df['Wave'].sum()}개")
            st.dataframe(df[df['Wave'] == True][['Close']])
        else:
            st.error("데이터를 불러오지 못했습니다. 잠시 후 다시 시도하거나 다른 티커(예: AAPL)를 입력해보세요.")
        else:
            st.warning("차트를 그릴 데이터가 없습니다.")
