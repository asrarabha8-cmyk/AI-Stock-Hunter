import streamlit as st
import pandas as pd
import yfinance as yf
import time

# إعداد الصفحة
st.set_page_config(
    page_title="AI Stock Hunter",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 AI Stock Hunter Dashboard")

# تحديث تلقائي
refresh = st.sidebar.slider(
    "Refresh (seconds)",
    30,
    300,
    60
)

symbols = [
    "ASTS","PL","RKLB","IONQ","SOUN",
    "HIMS","MSTR","AMD","NVDA",
    "SMCI","CRWD","PLTR","COIN",
    "RIVN","LCID"
]


def scan_market():

    results=[]

    for symbol in symbols:

        try:

            data = data = yf.download(
    symbol,
    period="1mo",
    interval="1d",
    progress=False,
    auto_adjust=True
)

if data.empty:
    continue

            if len(data)<20:
                continue


            price=float(data["Close"].iloc[-1])
            prev=float(data["Close"].iloc[-2])

            change=((price/prev)-1)*100


            volume=float(data["Volume"].iloc[-1])
            avg_volume=float(
                data["Volume"].tail(20).mean()
            )

            volume_x=volume/avg_volume


            score=0


            # Volume
            if volume_x>5:
                score+=40
            elif volume_x>3:
                score+=30
            elif volume_x>2:
                score+=20


            # Momentum
            if change>10:
                score+=30
            elif change>5:
                score+=20
            elif change>0:
                score+=10


            # Trend
            ma20=float(
                data["Close"].tail(20).mean()
            )

            if price>ma20:
                score+=20


            results.append([
                symbol,
                round(price,2),
                round(change,2),
                round(volume_x,2),
                score
            ])

        except:
            except Exception as e:
    st.write(symbol, e)


    df=pd.DataFrame(
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


# عرض البيانات

df=scan_market()


st.subheader("🔥 Top Momentum Stocks")

st.dataframe(
    df,
    use_container_width=True
)


st.caption(
    f"Last update: {time.strftime('%H:%M:%S')}"
)


# تحديث تلقائي
time.sleep(refresh)
st.rerun()