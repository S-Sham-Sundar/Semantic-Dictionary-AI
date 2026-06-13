import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()
genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

def generate_explanation(
    word,
    definition,
    semantic_words,
    graph_words
):

    prompt = f"""
    Explain this word in a clear and educational way.

    Word:
    {word}

    Dictionary Definition:
    {definition}

    Semantic Search Results:
    {", ".join(semantic_words)}

    Graph Related Words:
    {", ".join(graph_words)}

    Generate:
    1. Simple explanation
    2. Real-world meaning
    3. Connection to related concepts

    Keep response under 120 words.
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception:
        return "AI explanation temporarily unavailable."


