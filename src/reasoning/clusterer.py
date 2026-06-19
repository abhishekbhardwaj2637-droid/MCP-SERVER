import umap.umap_ as umap
import hdbscan
import numpy as np

def cluster_reviews(embeddings: list[list[float]], n_neighbors=15, min_cluster_size=15) -> list[int]:
    """
    Takes high-dimensional embeddings, reduces them with UMAP, 
    and clusters them with HDBSCAN.
    Returns a list of cluster labels (-1 means noise/unclustered).
    """
    print(f"Clustering {len(embeddings)} items...")
    
    # 1. Dimensionality Reduction (UMAP)
    # Reduce to a lower dimensional space (e.g. 5D) to make density clustering effective
    print("Running UMAP dimensionality reduction...")
    reducer = umap.UMAP(
        n_neighbors=n_neighbors, 
        n_components=5, 
        metric='cosine',
        random_state=42
    )
    reduced_embeddings = reducer.fit_transform(np.array(embeddings))
    
    # 2. Density-Based Clustering (HDBSCAN)
    print("Running HDBSCAN clustering...")
    clusterer = hdbscan.HDBSCAN(
        min_cluster_size=min_cluster_size,
        min_samples=5,
        metric='euclidean',
        cluster_selection_method='eom'
    )
    
    labels = clusterer.fit_predict(reduced_embeddings)
    
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise = list(labels).count(-1)
    print(f"Discovered {n_clusters} clusters. Noise points: {n_noise}")
    
    return labels.tolist()

def group_reviews_by_cluster(reviews: list[dict], labels: list[int]) -> dict[int, list[dict]]:
    """
    Groups the reviews into a dictionary where the key is the cluster label,
    and the value is the list of reviews belonging to that cluster.
    Ignores noise (-1).
    """
    clustered_data = {}
    for review, label in zip(reviews, labels):
        if label == -1:
            continue
        
        if label not in clustered_data:
            clustered_data[label] = []
        clustered_data[label].append(review)
        
    return clustered_data
