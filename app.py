import streamlit as st
import yfinance as yf
import pandas as pd

# 라이브러리 안전장치
try:
    import pandas_ta as ta
    has_ta = True
except ImportError:
    has_ta = False

st.title("엘리어트 파동 자동 분석기")

# 데이터 로드 함수
@st.cache_data
def load_data(ticker):
    df = yf.download(ticker, period="1y", interval="1d", auto_adjust=True)
    return df

ticker = st.text_input("티커 입력 (예: TSLA, AAPL)", "TSLA")

if ticker:
    df = load_data(ticker)

    # ZigZag 로직
    def get_zigzag(df, pct=0.05):
        df['pct_change'] = df['Close'].pct_change()
        df['ZigZag'] = df['pct_change'].abs() > pct
        return df

    df = get_zigzag(df)

    # 기술적 지표 (들여쓰기 교정 완료)
    if has_ta:
        df['RSI'] = ta.rsi(df['Close'], length=14)
        st.subheader("기술적 지표 (RSI & 거래량)")
        st.line_chart(df[['RSI']])
        st.bar_chart(df['Volume'])
    else:
        st.warning("분석 라이브러리(pandas_ta)가 없습니다. 기본 기능만 표시됩니다.")

    # 결과 출력
    st.line_chart(df['Close'])
    st.write("분석된 데이터 상단:", df.tail())
