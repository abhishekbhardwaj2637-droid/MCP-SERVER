from sentence_transformers import SentenceTransformer

class ReviewEmbedder:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        print(f"Loading embedding model: {model_name}...")
        self.model = SentenceTransformer(model_name)

    def embed(self, texts: list[str]) -> list[list[float]]:
        print(f"Generating embeddings for {len(texts)} texts...")
        # encode returns a numpy array, we can convert it to a list if needed
        embeddings = self.model.encode(texts, show_progress_bar=True)
        return embeddings.tolist()

def generate_embeddings(reviews: list[dict]) -> tuple[list[dict], list[list[float]]]:
    """
    Takes a list of reviews and generates embeddings for their content.
    Returns the reviews and their corresponding embeddings.
    """
    embedder = ReviewEmbedder()
    
    texts = [review.get("content", "") for review in reviews]
    embeddings = embedder.embed(texts)
    
    return reviews, embeddings
