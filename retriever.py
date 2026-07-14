import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import config
from sentence_transformers import SentenceTransformer

vectorizer = SentenceTransformer(config.EMBEDDING_MODEL)

# Embed documents using the specified embedding model
def embed_doc(documents):
    return vectorizer.encode(documents)

# Retrieve top-k relevant documents based on cosine similarity
def retrieve(question, documents, doc_vectors, k=config.RETRIEVAL_K):
    q_vector = vectorizer.encode([question])
    similarities = cosine_similarity(q_vector, doc_vectors)[0]
    top_k = np.argsort(similarities)[::-1][:k]
    return [(documents[i], similarities[i]) for i in top_k]