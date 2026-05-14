from llm import model
import pdfplumber

# 📄 Extract text from PDF
def extract_text_from_pdf(file):
    text = ""

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"

    return text.strip()


# 🤖 Chat with resume
def chat_with_resume(resume_text, user_question):
    
    if not resume_text:
        return "Resume not readable properly."

    prompt = f"""
You are a career advisor AI.

Resume:
{resume_text}

Question:
{user_question}

Give:
- clear answer
- strengths
- weaknesses
- improvements
"""

    response = model.generate_content(prompt)
    return response.text
