import json
from llm import model
import pdfplumber


# 📄 Extract text from PDF (same as resume.py)
def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    return text.strip()


# 🔍 Full Resume Analysis
def analyze_resume(resume_text, target_role=""):
    if not resume_text:
        return None

    role_context = f"Target Role: {target_role}" if target_role else "No specific target role given."

    prompt = f"""
You are an expert ATS resume analyzer and career coach.

Resume:
{resume_text}

{role_context}

Respond ONLY with valid JSON (no markdown, no extra text):
{{
  "ats_score": <number 0-100>,
  "experience_years": <number>,
  "skills_found": ["skill1", "skill2"],
  "skills_missing": ["skill1", "skill2"],
  "strengths": ["point1", "point2", "point3"],
  "weaknesses": ["point1", "point2", "point3"],
  "improvement_tips": "<specific tips paragraph>",
  "overall_analysis": "<detailed multi-paragraph analysis>"
}}
"""

    response = model.generate_content(prompt)
    raw = response.text

    # Clean and parse JSON
    cleaned = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(cleaned)
