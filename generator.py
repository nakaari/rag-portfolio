import config
from dotenv import load_dotenv
from google import genai
import os

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def rag_answer(question, context):
    # Send prompt to LLM for answer generation
    prompt = f"Question: {question}\nContext: {context}\nAnswer:"
    response = client.models.generate_content(
        model = config.LLM_MODEL,
        content = prompt
    )
    return response.text


