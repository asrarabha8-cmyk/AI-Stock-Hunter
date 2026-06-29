import streamlit as st
import pandas as pd
import yfinance as yf
import time
from streamlit_autorefresh import st_autorefresh
from fundamentals import get_fundamentals
st.set_page_config(
    page_title="AI Stock Hunter Pro",
    page_icon="🚀",
    layout="wide"
)
# =======================
# Sidebar
# =======================
st.sidebar.title("⚙️ AI Hunter Filters")
min_score = st.sidebar.slider(
    "Minimum AI Score",
    0,
    100,
    50
)
search_symbol = st.sidebar.text_input(
    "Search Symbol",
    ""
).upper()
only_hidden_gems = st.sidebar.checkbox(
    "🚀 Market Has Not Priced It Yet"
)
refresh_button = st.sidebar.button("🔄 Refresh")
# =======================
# Title
# =======================
st.title("🚀 AI Stock Hunter Pro")
# تحديث تلقائي كل دقيقة
st_autorefresh(interval=60000, key="refresh")
from symbols import SYMBOLS
symbols = SYMBOLS
@st.cache_data(ttl=300)
def scan_market():
    results = []
    for symbol in symbols:
        try:
            data = yf.Ticker(symbol).history(
                period="3mo"
            )
            if data.empty:
                continue
            stock = yf.Ticker(symbol)
            info = stock.info
            price = float(data["Close"].iloc[-1])
            old = float(data["Close"].iloc[-2])
            change = ((price / old) - 1) * 100
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
            fund = get_fundamentals(symbol)
            growth = fund["Growth"]
            quality = fund["Quality"]
            valuation = fund["Valuation"]
            sector = fund["Sector"]
            revenue_growth = info.get(
                "revenueGrowth", 0
            )
            if revenue_growth:
                revenue_growth = round(
                    revenue_growth * 100, 1
                )
            else:
                revenue_growth = 0
            pe = info.get("trailingPE", 0)
            if pe is None:
                pe = 0
            ps = info.get("priceToSalesTrailing12Months", 0)
            if ps is None:
                ps = 0
            final_score = (
                score +
                growth +
                quality +
                valuation
            )
            
            if final_score >= 75:
                signal = "🚀 STRONG"
            elif final_score >= 50:
                signal = "👀 WATCH"
            else:
                signal = "⌛ WAIT"

            hidden_gem = (
              revenue_growth > 20
               and final_score > 50
               and ps < 20
                )
            results.append([
                symbol,
                round(price,2),
                round(change,2),
                round(volume_x,2),
                revenue_growth,
                round(pe,1),
                round(ps,1),
                sector,
                final_score,
                signal,
                hidden_gem
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
            "Revenue Growth %",
            "P/E",
            "P/S",
            "Sector",
            "AI Score",
            "Signal",
            "Hidden Gem"
        ]
    )
    return df.sort_values(
        "AI Score",
        ascending=False
    )
df = scan_market()
# Filters
df = df[df["AI Score"] >= min_score]
if search_symbol:
    df = df[
        df["Symbol"].str.contains(
            search_symbol
        )
    ]
if only_hidden_gems:
    df = df[df["Hidden Gem"] == True]
st.subheader("🔥 AI Ranked Stocks")
st.dataframe(
    df,
    use_container_width=True
)
csv = df.to_csv(index=False)
st.download_button(
    "📥 Download CSV",
    csv,
    "ai_stock_hunter.csv",
    "text/csv"
)
st.caption(
    "Updated: " +
    time.strftime("%H:%M:%S")
)