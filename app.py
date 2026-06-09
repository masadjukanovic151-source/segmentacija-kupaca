import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from io import BytesIO

from data_processing import preprocess
from rfm import create_rfm
from clustering import run_clustering
from evaluation import evaluate_model

# =========================
# SETUP
# =========================
st.set_page_config(
    page_title="Segmentacija kupaca",
    layout="wide",
    page_icon="🛍️"
)

page = st.sidebar.selectbox(
    "📌 Navigacija",
    ["📊 Pregled", "🤖 HDBSCAN", "📈 GMM", "💰 CLV & ROI", "📅 Cohort", "🎯 What-if"]
)

uploaded_file = st.sidebar.file_uploader("📂 Učitaj CSV / Excel", type=["csv", "xlsx"])

# =========================
# FUNKCIJE
# =========================
def predict_segment(rec, freq, mon):
    if rec <= 90 and freq >= 10 and mon >= 1000:
        return "VIP kupac"
    elif freq >= 5:
        return "Aktivan kupac"
    else:
        return "Nizak učinak"

def calculate_clv(rfm):
    return (rfm["Monetary"] * rfm["Frequency"]) / (rfm["Recency"] + 1)

def calculate_roi(clv, cost=50):
    return (clv - cost) / cost * 100

# =========================
# LOAD DATA
# =========================
if uploaded_file:

    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith("csv") else pd.read_excel(uploaded_file)
    df = preprocess(df)

    rfm = create_rfm(df)

    # CLUSTERING (OBAVEZNO PRIJE UI PREVOĐENJA)
    rfm, scaled = run_clustering(rfm)

    rfm["HDBSCAN"] = rfm["HDBSCAN"].astype(int)
    rfm["GMM"] = rfm["GMM"].astype(int)

    score = evaluate_model(scaled, rfm["HDBSCAN"])

    # CLV
    rfm["CLV"] = calculate_clv(rfm)
    rfm["ROI"] = calculate_roi(rfm["CLV"])

    # =========================
    # PREVIEW (UI COPY)
    # =========================
    rfm_display = rfm.rename(columns={
        "Recency": "Dani od posljednje kupovine",
        "Frequency": "Koliko često kupuje",
        "Monetary": "Ukupna potrošnja kupca"
    })

    df_display = df.rename(columns={
        "InvoiceNo": "Broj fakture",
        "InvoiceDate": "Datum kupovine",
        "Quantity": "Količina",
        "UnitPrice": "Cijena",
        "CustomerID": "ID kupca"
    })

    # =========================
    # PREGLED
    # =========================
    if page == "📊 Pregled":

        st.title("📊 Pregled kupaca")

        col1, col2, col3 = st.columns(3)
        col1.metric("👥 Kupci", len(rfm))
        col2.metric("🧾 Narudžbe", df["InvoiceNo"].nunique())
        col3.metric("📊 Silhouette", round(score, 3))

        st.dataframe(rfm_display.head())
        st.dataframe(df_display.head())

    # =========================
    # HDBSCAN
    # =========================
    elif page == "🤖 HDBSCAN":

        st.title("🤖 HDBSCAN segmentacija")

        fig = px.scatter(
            rfm,
            x="Recency",
            y="Monetary",
            color=rfm["HDBSCAN"].astype(str),
            size="Frequency",
            template="plotly_white"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
        ### 🎨 HDBSCAN segmenti
        - 0 → VIP  
        - 1 → aktivni  
        - 2 → rijetki  
        - -1 → outlajeri  
        """)

    # =========================
    # GMM
    # =========================
    elif page == "📈 GMM":

        st.title("📈 GMM segmentacija")

        fig = px.scatter(
            rfm,
            x="Recency",
            y="Monetary",
            color=rfm["GMM"].astype(str),
            size="Frequency",
            template="plotly_white"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
        ### 🎨 GMM segmenti
        - 0 → VIP  
        - 1 → stabilni  
        - 2 → povremeni  
        """)

    # =========================
    # CLV & ROI
    # =========================
    elif page == "💰 CLV & ROI":

        st.title("💰 CLV i ROI analiza")

        st.metric("📊 Prosječan CLV", round(rfm["CLV"].mean(), 2))
        st.metric("📈 Prosječan ROI (%)", round(rfm["ROI"].mean(), 2))

        st.dataframe(rfm[["CLV", "ROI"]].head())

    # =========================
    # COHORT (FIXED)
    # =========================
    elif page == "📅 Cohort":

        st.title("📅 Cohort analiza")

        df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

        # FIX: Period -> STRING (rješava grešku)
        df["Month"] = df["InvoiceDate"].dt.to_period("M").astype(str)

        cohort = df.groupby("Month")["CustomerID"].nunique().reset_index()

        fig = px.line(
            cohort,
            x="Month",
            y="CustomerID",
            markers=True,
            template="plotly_white",
            labels={
                "Month": "Mjesec",
                "CustomerID": "Broj kupaca"
            }
        )

        st.plotly_chart(fig, use_container_width=True)

    # =========================
    # WHAT IF
    # =========================
    elif page == "🎯 What-if":

        st.title("🎯 Simulacija kupca")

        rec = st.slider("Recency", 0, 365, 50)
        freq = st.slider("Frequency", 1, 50, 5)
        mon = st.slider("Monetary", 0, 10000, 500)

        if st.button("Analiziraj"):
            st.success(f"👉 {predict_segment(rec, freq, mon)}")

else:
    st.title("🛍️ Segmentacija kupaca")
    st.info("Učitaj dataset za pokretanje sistema")