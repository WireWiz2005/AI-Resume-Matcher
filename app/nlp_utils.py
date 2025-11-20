# app/nlp_utils.py

import re
from typing import List, Dict, Set

import spacy

from .skills_data import get_all_skills

# Load spaCy English model once
nlp = spacy.load("en_core_web_sm")

# Preload skill vocabulary
SKILL_SET: Set[str] = get_all_skills()


def clean_text(text: str) -> str:
    """Basic text normalization."""
    if not text:
        return ""
    text = text.replace("\r", " ").replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_skills(text: str) -> List[str]:
    """
    Extract skills from text using a simple dictionary-based approach.
    """
    if not text:
        return []

    text_norm = clean_text(text).lower()
    found: Set[str] = set()

    # Direct phrase match
    for skill in SKILL_SET:
        if skill in text_norm:
            found.add(skill)

    # Token-based backup for single-word skills
    doc = nlp(text_norm)
    tokens = {token.text for token in doc}

    for skill in SKILL_SET:
        if " " not in skill and skill in tokens:
            found.add(skill)

    return sorted(found)


def extract_years_of_experience(text: str):
    """
    Rough heuristic to estimate years of experience from phrases like
    '2 years of experience', '3+ years', etc.
    """
    if not text:
        return None

    text_norm = clean_text(text).lower()

    pattern = r"(\d{1,2})\s*\+?\s*(years|year|yrs)"
    matches = re.findall(pattern, text_norm)

    if not matches:
        return None

    years = max(int(m[0]) for m in matches)
    return years


def build_resume_profile(text: str) -> Dict:
    """Build a structured view of the resume."""
    return {
        "skills": extract_skills(text),
        "years_of_experience": extract_years_of_experience(text),
    }


def build_job_profile(text: str) -> Dict:
    """Build a structured view of the job description."""
    return {
        "required_skills": extract_skills(text),
    }
