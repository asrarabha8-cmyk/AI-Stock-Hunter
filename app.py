import streamlit as st
import pandas as pd
import yfinance as yf
import time

st.set_page_config(
    page_title="AI Stock Hunter",
    page_icon="🚀"
)

st.title("🚀 AI Stock Hunter")

symbols = [
    "ASTS","PL","RKLB","IONQ",
    "SOUN","HIMS","MSTR",
    "AMD","NVDA","SMCI"
]


def scan_market():

    results = []

    for symbol in symbols:

        try:
            data = yf.Ticker(symbol).history(
                period="1mo"
            )

            if data.empty:
                continue

            price = data["Close"].iloc[-1]
            old = data["Close"].iloc[-2]

            change = ((price / old) - 1) * 100

            volume = data["Volume"].iloc[-1]
            avg = data["Volume"].tail(20).mean()

            volume_x = volume / avg

            score = 0

            if volume_x > 3:
                score += 40

            if change > 5:
                score += 30

            results.append([
                symbol,
                round(price,2),
                round(change,2),
                round(volume_x,2),
                score
            ])

        except Exception as e:
            st.write(symbol, e)

    return pd.DataFrame(
        results,
        columns=[
            "Symbol",
            "Price",
            "% Change",
            "Volume x",
            "Score"
        ]
    )


df = scan_market()

if df.empty:
    st.warning("No data received from Yahoo Finance")
else:
    st.dataframe(df)

st.caption(
    "Updated: " + time.strftime("%H:%M:%S")
)