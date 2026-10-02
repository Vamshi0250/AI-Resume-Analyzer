import os
import json
import re
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors, types

load_dotenv()

# Tried in order. If one is overloaded or unavailable, the next one is used.
MODELS = ["gemini-2.5-flash", "gemini-2.5-flash-lite", "gemini-2.0-flash"]
RETRIES_PER_MODEL = 3
RETRY_CODES = {429, 500, 503, 504}  # busy / temporary errors


def _get_api_key():
    """Read the key from .env locally, or from Streamlit secrets when deployed."""
    key = os.getenv("GEMINI_API_KEY")
    if key:
        return key
    try:
        import streamlit as st
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        return None


def _build_prompt(resume_text: str, job_description: str) -> str:
    return f"""
You are an expert ATS resume analyzer and career assistant.
Compare the resume with the job description.

RESUME:
\"\"\"{resume_text}\"\"\"

JOB DESCRIPTION:
\"\"\"{job_description}\"\"\"

Return ONLY a valid JSON object with exactly these keys:
{{
  "match_score": <integer 0-100>,
  "job_role": "<role title from the job description>",
  "summary": "<2-3 sentence overall assessment>",
  "matching_skills": ["..."],
  "missing_skills": ["..."],
  "partial_skills": ["..."],
  "matching_keywords": ["..."],
  "missing_keywords": ["..."],
  "experience_match": "<short explanation>",
  "education_match": "<short explanation>",
  "strengths": ["..."],
  "recommendations": ["..."]
}}

Rules:
- Be factual. Do not invent skills, experience, certifications or qualifications that are not in the resume.
- Use short items (1-4 words) for skills and keywords.
- Score guide: 80-100 strong match, 60-79 good, 40-59 average, below 40 weak.
"""


def _extract_json(text: str) -> dict:
    """Parse JSON even if the model wraps it in markdown fences."""
    text = text.strip()
    text = re.sub(r"^```(?:json)?|```$", "", text, flags=re.MULTILINE).strip()
    return json.loads(text)


def _call_with_retry(client, prompt: str) -> str:
    """Try each model, retrying busy errors with increasing waits."""
    last_error = None

    for model in MODELS:
        for attempt in range(RETRIES_PER_MODEL):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.2,
                        response_mime_type="application/json",
                    ),
                )
                if response.text:
                    return response.text
                last_error = ValueError("Empty response from model.")
            except errors.APIError as e:
                last_error = e
                if e.code in RETRY_CODES:
                    time.sleep(2 ** (attempt + 1))  # 2s, 4s, 8s
                    continue
                if e.code == 404:
                    break  # model name not available, go to next model
                raise  # bad key, bad request, etc. should be shown as is

    raise ValueError(
        "The Gemini service is very busy right now. Please wait a minute and try again."
    ) from last_error


def analyze_resume(resume_text: str, job_description: str) -> dict:
    api_key = _get_api_key()
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found. Add it to .env or Streamlit secrets.")

    client = genai.Client(api_key=api_key)
    raw = _call_with_retry(client, _build_prompt(resume_text, job_description))

    try:
        data = _extract_json(raw)
    except json.JSONDecodeError as e:
        raise ValueError("The AI returned an unreadable answer. Please try again.") from e

    # Make sure every key exists so the UI never breaks
    defaults = {
        "match_score": 0, "job_role": "N/A", "summary": "",
        "matching_skills": [], "missing_skills": [], "partial_skills": [],
        "matching_keywords": [], "missing_keywords": [],
        "experience_match": "", "education_match": "",
        "strengths": [], "recommendations": [],
    }
    for key, value in defaults.items():
        data.setdefault(key, value)

    data["match_score"] = max(0, min(100, int(data["match_score"])))
    return data