from groq import Groq
import os
from dotenv import load_dotenv
import re

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def clean_llm_output(output: str):

    # Remove markdown wrappers
    output = output.replace("```json", "")
    output = output.replace("```", "")

    output = output.strip()

    # Find JSON objects
    matches = re.findall(r'\{(?:[^{}]|(?:\{[^{}]*\}))*\}', output)

    # Return only the last valid JSON
    if matches:

        return matches[-1]

    return "{}"

def extract_data(user_input: str):

    prompt = f"""
You are a strict JSON generator.

Extract ONLY information explicitly mentioned by the user.

IMPORTANT RULES:
- NEVER invent data
- NEVER assume outcomes
- NEVER assume followup
- NEVER assume materials
- NEVER auto-generate attendees
- Missing fields MUST be ""

Return ONLY valid JSON.

FIELDS:
name, date, time, attendees, topics, materials, samples, sentiment, outcomes, followup, action

ALLOWED SENTIMENT VALUES:
positive
negative
neutral

EXAMPLE:

INPUT:
i met with dr vaish today and it was good positive and we discussed about the trendy drug in the market

OUTPUT:
{{
  "name": "Dr Vaish",
  "date": "today",
  "time": "",
  "attendees": "",
  "topics": "trendy drug in the market",
  "materials": "",
  "samples": "",
  "sentiment": "positive",
  "outcomes": "",
  "followup": "",
  "action": "log"
}}

INPUT:
edit sentiment to positive

OUTPUT:
{{
  "name": "",
  "date": "",
  "time": "",
  "attendees": "",
  "topics": "",
  "materials": "",
  "samples": "",
  "sentiment": "positive",
  "outcomes": "",
  "followup": "",
  "action": "edit"
}}

INPUT:
{user_input}
"""

    try:

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        raw_output = response.choices[0].message.content

        print("LLM RAW OUTPUT:", raw_output)

        cleaned_output = clean_llm_output(raw_output)

        print("LLM CLEANED OUTPUT:", cleaned_output)

        return cleaned_output

    except Exception as e:

        print("LLM ERROR:", e)

        return "{}"