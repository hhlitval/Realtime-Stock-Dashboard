import streamlit as st
import pandas as pd
import time
from pathlib import Path

CSV_PATH = Path(__file__).resolve().parent.parent / "data" / "stock_prices.csv"
st.title("Live Aktien Dashboard")
st.write("Daten werden live aus Kafka → Consumer → CSV geladen.")
refreshrate = st.slider("Aktualisierungs-Intervall (Sekunden)", 1, 10, 3)
placeholder = st.empty()

while True:
    if CSV_PATH.exists():
        df = pd.read_csv(CSV_PATH)

        # Letzte 200 Zeilen
        latest = df.tail(200)

        with placeholder.container():
            st.subheader("Live Stock Prices")
            st.line_chart(latest.pivot(index="timestamp", columns="symbol", values="price"))

            st.subheader("Letzte Datenpunkte")
            st.dataframe(latest.tail(10))
    else:
        st.warning("CSV existiert noch nicht. Starte Producer & Consumer.")

    time.sleep(refreshrate)
