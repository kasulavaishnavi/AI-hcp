from services.llm import extract_data
from services.tools import (
    log_interaction,
    edit_interaction,
    summarize_interaction,
    suggest_followup,
    reset_interaction
)

from db.connection import save, get
from datetime import datetime

import json


def run_agent(user_input: str):

    llm_output = extract_data(user_input)

    try:

        data = json.loads(llm_output)

        if isinstance(data, list):
            data = data[0]

    except Exception:

        return {
            "tool": "error",
            "data": {},
            "message": "Invalid LLM output"
        }

    # Clean extracted data
    data = clean_data(data)

    text = user_input.lower().strip()

    # Summarize tool
    if (
        "summarize" in text
        or "summary" in text
    ):

        return summarize_interaction(get())

    # Follow-up tool
    if (
        "follow up" in text
        or "followup" in text
        or "suggest follow up" in text
        or "suggestion" in text
    ):

        previous = get()

        # Remove empty values
        cleaned_followup_data = {}

        for key, value in data.items():

            if value not in ["", None]:

                cleaned_followup_data[key] = value

        # Merge safely
        merged = {
            **previous,
            **cleaned_followup_data
        }

        save(merged)

        return suggest_followup(merged)

    #Submit tool
    if (
        "submit" in text
        or "submit interaction" in text
        or "save interaction" in text
    ):

        submitted_data = get()

        save({})

        return {
            "tool": "submit_interaction",
            "message": "submitted successfully.",
            "data": {}
        }

    #Reset tool
    if (
        "reset" in text
        or "clear form" in text
    ):

        save({})

        return reset_interaction({})

    # edit action
    edit_keywords = ["change", "update", "edit", "modify"]

    if any(word in text for word in edit_keywords):

        action = "edit"

    else:

        action = "log"

    data["action"] = action

    # Remove empty values
    cleaned_data = {}

    for key, value in data.items():

        if value not in ["", None]:

            cleaned_data[key] = value

    # Previous stored data
    previous = get()

    # Merge data
    merged = {
        **previous,
        **cleaned_data
    }

    # Auto current date
    if merged.get("date") == "today":

        merged["date"] = datetime.now().strftime("%d-%m-%Y")

    # Auto current time
    if not merged.get("time"):

        merged["time"] = datetime.now().strftime("%H:%M")

    # Detect missing important fields
    missing_fields = []

    important_fields = [
        "name",
        "date",
        "topics",
        "sentiment",
        "materials",
        "followup"
    ]

    for field in important_fields:

        if not str(merged.get(field, "")).strip():

            missing_fields.append(field)

    # Humanfriendly questions
    follow_questions = []

    if "topics" in missing_fields:
        follow_questions.append("topics discussed")

    if "sentiment" in missing_fields:
        follow_questions.append("interaction sentiment")

    if "materials" in missing_fields:
        follow_questions.append("materials shared")

    if "followup" in missing_fields:
        follow_questions.append("follow-up actions")

    # Save merged result
    save(merged)

    # Return correct tool
    if action == "edit":

        response = edit_interaction(merged)

    else:

        response = log_interaction(merged)

    # prompt
    if follow_questions:

        response["assistant_message"] = (
            "Would you like to add "
            + ", ".join(follow_questions)
            + "?"
        )

    return response


def clean_data(data):

    #Clean name
    if "name" in data and data["name"]:

        data["name"] = (
            data["name"]
            .replace("Met ", "")
            .replace("met ", "")
            .replace("with ", "")
            .strip()
        )

    #Normalize sentiment
    if "sentiment" in data and data["sentiment"]:

        data["sentiment"] = data["sentiment"].lower()

    return data


