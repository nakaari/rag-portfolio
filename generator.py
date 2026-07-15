import config
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def rag_answer(question, context):
    # Send prompt to LLM for answer generation
    prompt = f"""
    If the answer isn't in the context, say 'I don't know'.
    Question: {question}
    Context: {context}
    Answer:
    """
    response = client.models.generate_content(
        model = config.LLM_MODEL,
        contents = prompt
    )
    return response.text


