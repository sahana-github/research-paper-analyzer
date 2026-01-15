from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

def cluster_papers(papers, num_clusters):
    abstracts = [p["summary"] for p in papers]

    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=1000
    )
    X = vectorizer.fit_transform(abstracts)

    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    labels = kmeans.fit_predict(X)

    clusters = {}
    for label, paper in zip(labels, papers):
        clusters.setdefault(label, []).append(paper)

    return clusters
