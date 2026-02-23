from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px

app = Flask(__name__)

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("data/crypto.csv")

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df = df.dropna(subset=["Date"])
df = df.sort_values("Date").reset_index(drop=True)

date_list = df["Date"].dt.strftime("%Y-%m-%d").tolist()


# =========================
@app.route("/", methods=["GET"])
def home():

    start_idx = request.args.get("start_idx", default=0, type=int)
    end_idx = request.args.get("end_idx", default=len(df)-1, type=int)

    filtered = df.iloc[start_idx:end_idx+1]

    if filtered.empty:
        filtered = df.copy()

    # ================= KPI =================
    latest_price = filtered["Close_Price"].iloc[-1]
    total_volume = filtered["Volume"].sum()
    avg_market_cap = filtered["Market_Cap"].mean() / 1e9

    # ================= CHARTS =================
    fig1 = px.line(filtered, x="Date", y="Close_Price",
                   title="Bitcoin Closing Price")

    fig2 = px.bar(filtered, x="Date", y="Volume",
                  title="Trading Volume")

    fig3 = px.line(filtered, x="Date",
                   y=["High_Price","Low_Price"],
                   title="High vs Low Price")

    fig4 = px.line(filtered, x="Date", y="Market_Cap",
                   title="Market Capitalization")

    return render_template(
        "index.html",
        latest_price=round(latest_price,2),
        total_volume=int(total_volume),
        avg_market_cap=round(avg_market_cap,2),
        chart1=fig1.to_html(False),
        chart2=fig2.to_html(False),
        chart3=fig3.to_html(False),
        chart4=fig4.to_html(False),
        total_rows=len(df),
        dates=date_list,
        start_idx=start_idx,
        end_idx=end_idx
    )


if __name__ == "__main__":
    app.run(debug=True)