# app/main.py

from __future__ import annotations

from typing import List, Optional, Dict

import tempfile

from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .nlp_utils import (
    clean_text,
    build_resume_profile,
    build_job_profile,
)
from .file_utils import extract_text


app = FastAPI(
    title="AI Resume Analyzer",
    description="Backend API for Resume Analyzer & Job Matching System",
    version="1.0.0",
)


# ---------- Pydantic models ---------- #

class AnalyzeRequest(BaseModel):
    resume_text: str
    job_description_text: str


class SkillsMatch(BaseModel):
    matched_skills: List[str]
    missing_skills: List[str]
    extra_resume_skills: List[str]


class AnalyzeResponse(BaseModel):
    overall_match_score: float
    skill_match_percentage: float
    text_similarity_score: float
    resume_profile: Dict
    job_profile: Dict
    skills_match: SkillsMatch
    notes: Optional[str] = None


class UploadAnalyzeResponse(AnalyzeResponse):
    extracted_text: str


# ---------- Helper functions ---------- #

def compute_text_similarity(resume_text: str, job_text: str) -> float:
    """
    Compute cosine similarity between resume and job description
    using TF-IDF. Returns a value in [0, 1].
    """
    resume_clean = clean_text(resume_text)
    job_clean = clean_text(job_text)

    if not resume_clean or not job_clean:
        return 0.0

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_features=5000,
    )
    matrix = vectorizer.fit_transform([resume_clean, job_clean])
    sim = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]
    return float(sim)


def compute_skill_match(resume_skills: List[str], job_skills: List[str]) -> SkillsMatch:
    resume_set = set(resume_skills)
    job_set = set(job_skills)

    matched = sorted(resume_set & job_set)
    missing = sorted(job_set - resume_set)
    extra = sorted(resume_set - job_set)

    return SkillsMatch(
        matched_skills=matched,
        missing_skills=missing,
        extra_resume_skills=extra,
    )


def combine_scores(text_sim: float, skill_match_pct: float) -> float:
    """
    Combine text similarity [0,1] and skill match percentage [0,100]
    into a final score [0,100]. Weighted 60% skills, 40% text similarity.
    """
    skill_norm = skill_match_pct / 100.0
    combined = 0.6 * skill_norm + 0.4 * text_sim
    return round(combined * 100, 2)


def run_analysis(resume_text: str, job_description_text: str) -> AnalyzeResponse:
    """
    Core analysis logic reused by both /analyze and /upload-and-analyze.
    """
    # Build semantic profiles
    resume_profile = build_resume_profile(resume_text)
    job_profile = build_job_profile(job_description_text)

    resume_skills = resume_profile.get("skills", [])
    job_skills = job_profile.get("required_skills", [])

    # Skill-based matching
    skills_match = compute_skill_match(resume_skills, job_skills)

    # Skill match percentage
    if job_skills:
        skill_match_pct = round(
            100.0 * len(skills_match.matched_skills) / len(job_skills), 2
        )
    else:
        skill_match_pct = 0.0

    # Text similarity
    text_sim = compute_text_similarity(resume_text, job_description_text)

    # Final combined score
    overall_score = combine_scores(text_sim, skill_match_pct)

    # Notes
    notes_parts = []
    if skills_match.missing_skills:
        notes_parts.append(
            "Consider learning or explicitly mentioning these skills: "
            + ", ".join(skills_match.missing_skills)
            + "."
        )

    if overall_score < 50:
        notes_parts.append(
            "Overall match is low. You may need to tailor your resume more closely to this role."
        )
    elif overall_score < 75:
        notes_parts.append(
            "Decent match. Highlight key relevant projects and skills to strengthen your application."
        )
    else:
        notes_parts.append(
            "Strong match. Ensure your achievements are quantified and clearly described."
        )

    notes = " ".join(notes_parts) if notes_parts else None

    return AnalyzeResponse(
        overall_match_score=overall_score,
        skill_match_percentage=skill_match_pct,
        text_similarity_score=round(text_sim, 3),
        resume_profile=resume_profile,
        job_profile=job_profile,
        skills_match=skills_match,
        notes=notes,
    )


# ---------- API endpoints ---------- #

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "API is running"}


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_resume(request: AnalyzeRequest):
    """
    Analyze plain text resume + job description.
    """
    return run_analysis(request.resume_text, request.job_description_text)


@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    """
    Upload a PDF/DOCX resume and return extracted text only.
    Useful for debugging.
    """
    temp = tempfile.NamedTemporaryFile(delete=False)
    temp.write(await file.read())
    temp.close()

    try:
        text = extract_text(temp.name)
    except Exception as e:
        return {"error": str(e)}

    return {"extracted_text": text}


@app.post("/upload-and-analyze", response_model=UploadAnalyzeResponse)
async def upload_and_analyze_resume(
    file: UploadFile = File(...),
    job_description_text: str = Form(...),
):
    """
    Upload a PDF/DOCX resume + job description text
    and return full analysis.
    """
    # Save uploaded file temporarily
    temp = tempfile.NamedTemporaryFile(delete=False)
    temp.write(await file.read())
    temp.close()

    # Extract text from resume
    try:
        resume_text = extract_text(temp.name)
    except Exception as e:
        # Fall back with error message
        return UploadAnalyzeResponse(
            extracted_text="",
            overall_match_score=0.0,
            skill_match_percentage=0.0,
            text_similarity_score=0.0,
            resume_profile={},
            job_profile={},
            skills_match=SkillsMatch(
                matched_skills=[],
                missing_skills=[],
                extra_resume_skills=[],
            ),
            notes=f"Failed to extract resume text: {e}",
        )

    analysis = run_analysis(resume_text, job_description_text)
    # Merge analysis fields and extracted text
    return UploadAnalyzeResponse(
        extracted_text=resume_text,
        **analysis.dict(),
    )
