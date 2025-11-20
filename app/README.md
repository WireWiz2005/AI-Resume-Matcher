# AI-Driven Resume Analyzer & Job Match System

An AI-powered backend service that analyzes a candidate's resume against a job description and returns a match score, skill gap analysis, and recommendations.

Built with **FastAPI**, **spaCy**, and **scikit-learn**.

---

## 🚀 Features

- Analyze **resume text** and **job description** text.
- Upload resume as **PDF** or **DOCX** and automatically extract text.
- Extracts and compares **technical skills** (Python, SQL, AWS, etc.).
- Calculates:
  - ✅ Overall match score (0–100)
  - ✅ Skill match percentage
  - ✅ Text similarity using TF-IDF + cosine similarity
  - ✅ Matched, missing, and extra skills
- Clean, documented REST API with Swagger UI at `/docs`.

---

## 🧱 Tech Stack

- **Backend:** Python, FastAPI
- **NLP:** spaCy (`en_core_web_sm`)
- **ML / Similarity:** scikit-learn (TF-IDF, cosine similarity)
- **File Parsing:** pdfplumber (PDF), python-docx (DOCX)
- **Data Handling:** NumPy, Pandas

---

## 📁 Project Structure

```text
AI-Resume-Matcher/
├─ app/
│  ├─ __init__.py
│  ├─ main.py            # FastAPI app + endpoints
│  ├─ nlp_utils.py       # Text cleaning, skill extraction, profiles
│  ├─ skills_data.py     # Predefined skill vocabulary
│  └─ file_utils.py      # PDF/DOCX text extraction
├─ venv/                 # Virtual environment (local only)
├─ requirements.txt
└─ README.md
