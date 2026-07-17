import config
import pdf_loader
import retriever
import generator

documents = pdf_loader.extract_sections(config.PDF_PATH)
document_texts = [section["text"] for section in documents]
doc_vectors = retriever.embed_doc(document_texts)

for question in ["What's offside?", "Can players use hands?"]:
    hits = retriever.retrieve(question, document_texts, doc_vectors)
    context = "\n".join(doc_text for doc_text, _ in hits)
    answer = generator.rag_answer(question, context)
    print(f"Question: {question}\nAnswer: {answer}\n")