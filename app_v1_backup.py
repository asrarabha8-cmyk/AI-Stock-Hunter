import streamlit as st
import pandas as pd
import yfinance as yf
import time
from fundamentals import get_fundamentals
st.set_page_config(
    page_title="AI Stock Hunter",
    page_icon="🚀",
    layout="wide"
)
st.title("🚀 AI Stock Hunter Dashboard")
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
            change = ((price / old) - 1) * 100
            volume = float(data["Volume"].iloc[-1])
            avg_volume = float(data["Volume"].tail(20).mean())
            volume_x = volume / avg_volume
            ma20 = float(
                data["Close"].tail(20).mean()
            )
            score = 0
            # Volume Score
            if volume_x >= 5:
                score += 40
            elif volume_x >= 3:
                score += 30
            elif volume_x >= 2:
                score += 20
            # Momentum Score
            if change >= 10:
                score += 30
            elif change >= 5:
                score += 20
            elif change > 0:
                score += 10
            # Trend Score
            if price > ma20:
                score += 20
            # Fundamentals
            fund = get_fundamentals(symbol)
            growth = fund["Growth"]
            quality = fund["Quality"]
            valuation = fund["Valuation"]
            sector = fund["Sector"]
            final_score = (
                score +
                growth +
                quality +
                valuation
            )
            results.append([
                symbol,
                round(price, 2),
                round(change, 2),
                round(volume_x, 2),
                growth,
                quality,
                valuation,
                sector,
                final_score
            ])
        except Exception as e:
            st.write(symbol, e)
    df = pd.DataFrame(
        results,
        columns=[
            "Symbol",
            "Price",
            "% Change",
            "Volume x",
            "Growth",
            "Quality",
            "Valuation",
            "Sector",
            "AI Score"
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
    "Last update: " +
    time.strftime("%H:%M:%S")
)