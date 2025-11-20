# app/skills_data.py

CORE_SKILLS = {
    # Programming Languages
    "python", "java", "c", "c++", "c#", "javascript",
    "typescript", "go", "rust", "php", "r", "sql",

    # Data / Machine Learning
    "machine learning", "deep learning", "nlp",
    "data analysis", "data analytics", "data engineering",
    "statistics", "eda", "computer vision",

    # Python Libraries
    "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch",
    "matplotlib", "seaborn",

    # Databases
    "mysql", "postgresql", "mongodb", "redis",

    # Cloud / DevOps
    "aws", "azure", "gcp", "docker", "kubernetes",
    "ci/cd", "git", "github",

    # General / soft skills
    "problem solving", "teamwork", "communication",
    "leadership", "api development", "rest api",
}


def get_all_skills():
    """
    Return all skills in lowercase.
    Expand this list over time as needed.
    """
    return {skill.lower() for skill in CORE_SKILLS}
