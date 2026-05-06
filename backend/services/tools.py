from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def log_interaction(data):

    return {
        "tool": "log_interaction",
        "data": data
    }


def edit_interaction(data):

    return {
        "tool": "edit_interaction",
        "data": data
    }


def summarize_interaction(data):

    summary = (
        f"Meeting with {data.get('name')} regarding "
        f"{data.get('topics')} was "
        f"{data.get('sentiment')}."
    )

    return {
        "tool": "summarize_interaction",
        "summary": summary
    }


def suggest_followup(data):

    prompt = f"""
You are an AI CRM assistant.

Interaction details:
Doctor: {data.get('name')}
Topics: {data.get('topics')}
Sentiment: {data.get('sentiment')}

Generate ONE SHORT professional follow-up action.

RULES:
- Maximum 12 words
- Do NOT explain
- Do NOT greet
- Do NOT use quotes
- Output ONLY the action sentence
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.5
    )

    suggestion = response.choices[0].message.content.strip()

    data["followup"] = suggestion

    return {
        "tool": "suggest_followup",
        "suggestion": suggestion,
        "data": data
    }


def reset_interaction(data):

    return {
        "tool": "reset",
        "data": {}
    }