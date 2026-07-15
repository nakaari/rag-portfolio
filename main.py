import config
import retriever
import generator

documents = [
    "our company refund policy allows returns within 30 days of purchase with a receipt.",
    "To reset your password, click 'Forgot Password' on the login page and check your email",
    "Customer support can be reacched at support@example.com or by phone at 555-0199.",
    "Our premium plan costs $20 per month and includes unlimited storage and priority support.",
]
doc_vectors = retriever.embed_doc(documents)

for question in ["What's the refund policy?", "How do I reset my password?"]:
    hits = retriever.retrieve(question, documents, doc_vectors)
    context = "\n".join(doc_text for doc_text, _ in hits)
    answer = generator.rag_answer(question, context)
    print(f"Question: {question}\nAnswer: {answer}\n")