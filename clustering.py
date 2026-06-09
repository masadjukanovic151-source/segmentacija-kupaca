import pandas as pd
import hdbscan
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler


def run_clustering(rfm, min_cluster_size=8, gmm_components=4):
    features = rfm[["Recency", "Frequency", "Monetary"]]
    scaler = StandardScaler()
    scaled = scaler.fit_transform(features)

    hdb = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size)
    labels_hdb = hdb.fit_predict(scaled)

    gmm = GaussianMixture(n_components=gmm_components, random_state=42)
    labels_gmm = gmm.fit_predict(scaled)

    result = rfm.copy()
    result["HDBSCAN"] = labels_hdb.astype(int)
    result["GMM"] = labels_gmm.astype(int)
    return result, scaled