# AI-Driven Resume Analyzer & Job Match System

A backend application that analyzes a candidate’s resume against a job description and generates a detailed match score. The system extracts skills, checks experience, compares text similarity, and highlights missing or matched skills. It also supports PDF and DOCX resume uploads with automatic text extraction.

---

## Features

- Extracts technical and soft skills from resume text  
- Detects years of experience  
- Compares resume with job description  
- Skill match percentage  
- Text similarity using TF-IDF  
- Missing and matched skills  
- Improvement suggestions  
- Upload and read PDF/DOCX resumes  
- Interactive API testing through Swagger UI  

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Check API status |
| POST | `/analyze` | Analyze resume text + job description |
| POST | `/upload-resume` | Upload resume and extract text |
| POST | `/upload-and-analyze` | Upload resume + full analysis |

---

## Installation

```bash
git clone https://github.com/WireWiz2005/AI-Resume-Matcher.git
cd AI-Resume-Matcher

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
python -m spacy download en_core_web_sm

uvicorn app.main:app --reload
AI-Resume-Matcher/
│── app/
│   ├── main.py
│   ├── nlp_utils.py
│   ├── file_utils.py
│   ├── skills_data.py
│   └── __init__.py
│── requirements.txt
│── README.md
│── .gitignore
