# RAG Portfolio Project

A modular Retrieval-Augmented Generation (RAG) system that answers football rules
questions by retrieving relevant passages from the official **IFAB Laws of the
Game** and generating grounded answers with the Gemini API.

This project started as a Google Colab notebook and was rewritten into a
modular, testable Python codebase to demonstrate real software engineering
practices applied to an LLM pipeline.

## What it does

1. Parses the official IFAB Laws of the Game PDF into structured sections
   (one per Law, plus supporting sections like the Glossary and VAR protocol)
2. Embeds each section using a sentence-transformer model
3. Given a user question, retrieves the most relevant sections via cosine
   similarity
4. Sends the retrieved context to Gemini, with an explicit instruction to
   answer only from the provided context — reducing hallucination

## Architecture

```
config.py       Single source of truth for constants (model names, k, paths)
pdf_loader.py   Parses the PDF into labeled sections (e.g. "Law 11")
retriever.py    Embeds documents and retrieves top-k relevant sections
generator.py    Sends context + question to Gemini and returns the answer
main.py         Orchestrates the full pipeline end to end
```

Each module has a single responsibility and can be tested independently —
for example, `retriever.py` can be checked for correct retrieval without
needing a valid Gemini API key or network access.

## Setup

**1. Clone the repo and create a virtual environment**
```bash
git clone https://github.com/nakaari/rag-portfolio.git
cd rag-portfolio
python3 -m venv .venv
source .venv/bin/activate
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Get the source document**

Download the current **Laws of the Game** (single-page PDF layout) from
IFAB's official site: https://www.theifab.com/laws-of-the-game-documents/

Place it in a `data/` folder in the project root. Update `PDF_PATH` in
`config.py` if your filename differs from the default.

> The PDF itself is not included in this repository, since it's IFAB's
> copyrighted publication — only freely available for direct download.

**4. Set up your Gemini API key**

Create a `.env` file in the project root (never committed to git):
```
GEMINI_API_KEY=your-api-key-here
```

## Usage

```bash
python3 main.py
```

This runs a small set of example questions through the full pipeline and
prints the retrieved-context-grounded answers.

Example:
```
Question: What's offside?
Answer: Based on the provided context, offside is governed by Law 11...
```

To ask your own questions, edit the `question` list in `main.py`, or import
the modules directly:

```python
import config, pdf_loader, retriever, generator

documents = pdf_loader.extract_sections(config.PDF_PATH)
document_texts = [section["text"] for section in documents]
doc_vectors = retriever.embed_doc(document_texts)

hits = retriever.retrieve("your question here", document_texts, doc_vectors)
context = "\n".join(doc_text for doc_text, _ in hits)
answer = generator.rag_answer("your question here", context)
print(answer)
```

## Notes on design decisions

- **Chunking by document structure, not fixed size**: sections are split by
  the PDF's own running header (`Law X | ...`) rather than arbitrary word
  counts, so each embedded chunk represents one coherent topic rather than a
  blurry average of several.
- **Anti-hallucination guardrail**: the prompt explicitly instructs the model
  to say it doesn't know if the answer isn't in the retrieved context, rather
  than falling back on its own general knowledge.
- **Single source of truth for constants**: model names, retrieval `k`, and
  file paths live only in `config.py`, so changes propagate without touching
  logic in other files.

## Tech stack

- `sentence-transformers` (`all-MiniLM-L6-v2`) for embeddings
- `scikit-learn` for cosine similarity
- `pypdf` for PDF text extraction
- Gemini API (`gemini-flash-latest`) for generation
- `python-dotenv` for local secret management

