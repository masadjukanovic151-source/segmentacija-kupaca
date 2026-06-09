import pandas as pd


def create_rfm(df):
    snapshot_date = df["InvoiceDate"].max()
    rfm = df.groupby("CustomerID").agg(
        Recency=("InvoiceDate", lambda x: (snapshot_date - x.max()).days),
        Frequency=("InvoiceNo", "nunique"),
        Monetary=("TotalPrice", "sum"),
    ).reset_index()
    rfm["Recency"] = rfm["Recency"].astype(int)
    return rfm