import streamlit as st
import pandas as pd
import yfinance as yf
import time

st.set_page_config(
    page_title="AI Stock Hunter",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 AI Stock Hunter Dashboard")

symbols = [
    "ASTS","PL","RKLB","IONQ","SOUN",
    "HIMS","MSTR","AMD","NVDA",
    "SMCI","CRWD","PLTR","COIN",
    "RIVN","LCID"
]



            def scan_market():

    results = []

    for symbol in symbols:

        try:
            data = yf.Ticker(symbol).history(
                period="1mo",
                interval="1d"
            )

            if data.empty:
                continue

            close = float(data["Close"].iloc[-1])
            previous = float(data["Close"].iloc[-2])

            change = ((close / previous) - 1) * 100

            volume = float(data["Volume"].iloc[-1])
            avg_volume = float(data["Volume"].tail(20).mean())

            volume_x = volume / avg_volume if avg_volume else 0

            ma20 = float(data["Close"].tail(20).mean())

            score = 0

            if volume_x >= 5:
                score += 40
            elif volume_x >= 3:
                score += 30
            elif volume_x >= 2:
                score += 20

            if change >= 10:
                score += 30
            elif change >= 5:
                score += 20
            elif change > 0:
                score += 10

            if close > ma20:
                score += 20

            results.append([
                symbol,
                round(close,2),
                round(change,2),
                round(volume_x,2),
                score
            ])

        except Exception as e:
            st.write("Error:", symbol, e)

    df = pd.DataFrame(
        results,
        columns=[
            "Symbol",
            "Price",
            "% Change",
            "Volume x",
            "AI Score"
        ]
    )

    return df.sort_values(
        "AI Score",
        ascending=False
    )


    df = pd.DataFrame(
        results,
        columns=[
            "Symbol",
            "Price",
            "% Change",
            "Volume x",
            "AI Score"
        ]
    )

    return df.sort_values(
        "AI Score",
        ascending=False
    )


df = scan_market()

st.subheader("🔥 Top Momentum Stocks")

if df.empty:
    st.warning("No data received from Yahoo Finance")
else:
    st.dataframe(
        df,
        use_container_width=True
    )


st.caption(
    "Updated: " + time.strftime("%H:%M:%S")
)