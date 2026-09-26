import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Stock Price Tracker", page_icon="📈", layout="wide")
 
st.title("📈 Stock & Crypto Price Tracker")
st.markdown("Track live prices and historical trends for any stock or cryptocurrency ticker.")


# --- Sidebar Inputs ---
st.sidebar.header("Settings")
ticker = st.sidebar.text_input("Enter ticker symbol", "AAPL").upper()
period = st.sidebar.selectbox(
    "Time period",
    ["1mo", "3mo", "6mo", "1y", "5y", "max"],
    index=2
)


# --- Fetch Data ---
try:
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
 
    if data.empty:
        st.error("No data found for this ticker. Check the symbol and try again.")
        st.stop()
 
    info = stock.info
    current_price = data["Close"].iloc[-1]
    prev_price = data["Close"].iloc[-2] if len(data) > 1 else current_price
    price_change = current_price - prev_price
    pct_change = (price_change / prev_price * 100) if prev_price != 0 else 0
 
    # --- KPIs ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Current Price", f"${current_price:,.2f}", f"{price_change:+.2f}")
    col2.metric("Change (%)", f"{pct_change:+.2f}%")
    col3.metric("Period High", f"${data['High'].max():,.2f}")
 
    st.markdown("---")
 
    # --- Price Chart ---
    st.subheader(f"{ticker} Closing Price ({period})")
    st.line_chart(data["Close"])
 
    # --- Volume Chart ---
    st.subheader("Trading Volume")
    st.bar_chart(data["Volume"])
 
    # --- Raw Data ---
    with st.expander("View Raw Data"):
        st.dataframe(data, use_container_width=True)
 
except Exception as e:
    st.error(f"Something went wrong: {e}")
 