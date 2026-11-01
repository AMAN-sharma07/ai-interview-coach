import json
import os
from google import genai
from google.genai import types

# Current stable Flash-class Gemini model string from official Google AI docs
GEMINI_MODEL = "gemini-3.8-flash"


# Send the question and transcript to Gemini and return structured JSON feedback
def get_feedback(question, transcript_text):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return {
            "rating": 0,
            "strengths": ["Missing GEMINI_API_KEY environment variable."],
            "improved_answer": "Error: Please set the GEMINI_API_KEY environment variable and try again.",
        }

    prompt = (
        f"You are an interview coach. Evaluate this spoken answer.\n"
        f"Question: {question}\n"
        f"Answer: {transcript_text}\n\n"
        f"Reply ONLY in valid JSON with this exact format:\n"
        f'{{"rating": 8, "strengths": ["point 1", "point 2", "point 3"], "improved_answer": "sample answer"}}'
    )

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(response_mime_type="application/json"),
        )
        data = json.loads(response.text.strip())
        return {
            "rating": max(1, min(10, int(data.get("rating", 5)))),
            "strengths": [str(s) for s in data.get("strengths", [])][:3],
            "improved_answer": str(data.get("improved_answer", "")).strip(),
        }
    except Exception as e:
        return {
            "rating": 0,
            "strengths": ["Could not parse or retrieve Gemini feedback."],
            "improved_answer": f"Friendly Error: Unable to get AI feedback right now ({e}).",
        }