import pandas as pd

REQUIRED_COLUMNS = ["CustomerID", "InvoiceNo", "InvoiceDate", "Quantity", "UnitPrice"]


def preprocess(df):
    df = df.copy()
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Nedostaju sledeće kolone: {', '.join(missing)}")

    df = df.dropna(subset=["CustomerID", "InvoiceDate"])
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")
    df = df.dropna(subset=["Quantity", "UnitPrice"])
    df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)]
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
    df = df.dropna(subset=["InvoiceDate"])
    df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]
    df = df[df["TotalPrice"] > 0]
    return df