from sklearn.metrics import silhouette_score


def evaluate_model(data, labels):
    unique_labels = set(labels)
    if len(unique_labels) > 1 and len(data) > 1:
        return float(silhouette_score(data, labels))
    return 0.0