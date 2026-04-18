import streamlit as st
import yfinance as yf
import pandas as pd

# 1. 대상 종목 리스트 (예시: S&P 500 + Nasdaq 100 중복 제거)
# 실제로는 S&P 500 ticker 리스트를 불러와서 처리합니다.
tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA'] 

def get_ticker_data(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    
    # 데이터 로드 (월봉, 주봉, 일봉)
    df_m = yf.download(ticker, period="5y", interval="1mo", progress=False)
    df_w = yf.download(ticker, period="2y", interval="1wk", progress=False)
    df_d = yf.download(ticker, period="1y", interval="1d", progress=False)
    
    # 1. 월봉 매물대 중심 (VWAP)
    vwap = (df_m['Volume'] * ((df_m['High'] + df_m['Low'] + df_m['Close']) / 3)).sum() / df_m['Volume'].sum()
    
    # 2. 기관 보유 비중
    inst_own = info.get('institutionalOwnershipPercent', 0)
    
    # 3. 40주 이평선 (주봉 기준)
    ma40_w = df_w['Close'].rolling(window=40).mean().iloc[-1]
    
    # 4. RSI (일봉, 주봉)
    def get_rsi(df, period=14):
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs.iloc[-1]))

    return {
        'Ticker': ticker,
        'Above_VWAP': df_d['Close'].iloc[-1] > vwap,
        'Inst_Own': inst_own,
        'Above_MA40W': df_w['Close'].iloc[-1] > ma40_w,
        'RSI_Daily': get_rsi(df_d),
        'RSI_Weekly': get_rsi(df_w)
    }

# 실행
results = [get_ticker_data(t) for t in tickers]
df_final = pd.DataFrame(results)

# 조건에 맞는 종목 필터링 (OR 조건 적용)
final_list = df_final[df_final['Above_VWAP'] == True]
st.dataframe(final_list)
