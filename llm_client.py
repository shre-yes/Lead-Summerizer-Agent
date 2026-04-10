import logging
from typing import Dict
from groq import Groq

logger = logging.getLogger(__name__)

def summarize_lead(client: Groq, model: str, row: Dict[str, str]) -> str:
    """
    Calls the Groq LLM to summarize a lead's info in 1-2 lines.
    """
    name = row.get("name") or "Unknown Name"
    company = row.get("company") or "Unknown Company"
    note = row.get("note") or "No note provided"

    system_prompt = (
        "You are a sales assistant. "
        "Summarize each lead in 1–2 short sentences, focusing on who they are, "
        "what they do, and any key points from their note. Do not invent details."
    )
    user_prompt = (
        f"Name: {name}, Company: {company}, Note: {note}. "
        "Summarize this lead in 1–2 short lines."
    )

    try:
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            model=model,
            temperature=0.3,
            max_tokens=100,
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Failed to summarize lead for {name}: {e}")
        return "<ERROR: failed to summarize>"
