import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np # 데이터 정제용

def get_clean_metrics(ticker):
    try:
        df_m = yf.download(ticker, period="3y", interval="1mo", progress=False)
        df_d = yf.download(ticker, period="3y", interval="1d", progress=False)
        
        # 1. 데이터가 비어있거나, 무한대/결측치가 있으면 제거
        if df_m.empty or df_d.empty: return None
        df_d = df_d.replace([np.inf, -np.inf], np.nan).dropna()
        
        vwap = (df_m['Volume'] * ((df_m['High'] + df_m['Low'] + df_m['Close']) / 3)).sum() / df_m['Volume'].sum()
        
        return {
            'Ticker': ticker,
            'Price': float(df_d['Close'].iloc[-1]), # 강제 형변환
            'VWAP': float(vwap),
            'Above_VWAP': bool(df_d['Close'].iloc[-1] > vwap) # 강제 형변환
        }
    except:
        return None
