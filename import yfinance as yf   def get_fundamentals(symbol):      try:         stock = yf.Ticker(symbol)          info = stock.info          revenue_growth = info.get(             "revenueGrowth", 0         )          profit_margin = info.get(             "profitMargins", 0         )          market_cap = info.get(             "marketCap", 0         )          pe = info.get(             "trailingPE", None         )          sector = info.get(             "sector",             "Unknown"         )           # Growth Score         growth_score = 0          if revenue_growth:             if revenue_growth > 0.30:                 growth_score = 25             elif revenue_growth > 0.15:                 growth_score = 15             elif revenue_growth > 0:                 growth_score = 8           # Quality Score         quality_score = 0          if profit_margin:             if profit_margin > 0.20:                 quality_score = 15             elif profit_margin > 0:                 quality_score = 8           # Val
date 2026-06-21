import yfinance as yf


def get_fundamentals(symbol):

    try:
        stock = yf.Ticker(symbol)

        info = stock.info

        revenue_growth = info.get(
            "revenueGrowth", 0
        )

        profit_margin = info.get(
            "profitMargins", 0
        )

        market_cap = info.get(
            "marketCap", 0
        )

        pe = info.get(
            "trailingPE", None
        )

        sector = info.get(
            "sector",
            "Unknown"
        )


        # Growth Score
        growth_score = 0

        if revenue_growth:
            if revenue_growth > 0.30:
                growth_score = 25
            elif revenue_growth > 0.15:
                growth_score = 15
            elif revenue_growth > 0:
                growth_score = 8


        # Quality Score
        quality_score = 0

        if profit_margin:
            if profit_margin > 0.20:
                quality_score = 15
            elif profit_margin > 0:
                quality_score = 8


        # Valuation Score
        valuation_score = 0

        if pe:
            if pe < 25:
                valuation_score = 20
            elif pe < 50:
                valuation_score = 10


        return {
            "Growth": growth_score,
            "Quality": quality_score,
            "Valuation": valuation_score,
            "Sector": sector
        }


    except:

        return {
            "Growth":0,
            "Quality":0,
            "Valuation":0,
            "Sector":"Unknown"
        }