import streamlit as st
import pandas as pd
import yfinance as yf
import time

st.set_page_config(
    page_title="AI Stock Hunter",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 AI Stock Hunter")

symbols = [
    "ASTS","PL","RKLB","IONQ",
    "SOUN","HIMS","MSTR",
    "AMD","NVDA","SMCI",
    "PLTR","COIN","RIVN"
]


def scan_market():

    results = []

    for symbol in symbols:

        try:
            data = yf.Ticker(symbol).history(
                period="3mo"
            )

            if data.empty:
                continue

            price = float(data["Close"].iloc[-1])
            old = float(data["Close"].iloc[-2])

            change = ((price / old)-1)*100

            volume = float(data["Volume"].iloc[-1])
            avg_volume = float(
                data["Volume"].tail(20).mean()
            )

            volume_x = volume / avg_volume


            ma20 = float(
                data["Close"].tail(20).mean()
            )


            score = 0


            # Volume
            if volume_x >= 5:
                score += 40
            elif volume_x >= 3:
                score += 30
            elif volume_x >= 2:
                score += 20


            # Momentum
            if change >= 10:
                score += 30
            elif change >= 5:
                score += 20
            elif change > 0:
                score += 10


            # Trend
            if price > ma20:
                score += 20


            # Signal

            if score >= 75:
                signal = "🚀 STRONG"
            elif score >= 50:
                signal = "👀 WATCH"
            else:
                signal = "⏳ WAIT"


            results.append([
                symbol,
                round(price,2),
                round(change,2),
                round(volume_x,2),
                score,
                signal
            ])


        except:
            pass


    df = pd.DataFrame(
        results,
        columns=[
            "Symbol",
            "Price",
            "% Change",
            "Volume x",
            "AI Score",
            "Signal"
        ]
    )


    return df.sort_values(
        "AI Score",
        ascending=False
    )



df = scan_market()


st.subheader("🔥 AI Ranked Stocks")


if df.empty:
    st.warning("No data")
else:
    st.dataframe(
        df,
        use_container_width=True
    )


st.caption(
    "Last update: " + time.strftime("%H:%M:%S")
)