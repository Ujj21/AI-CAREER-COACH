import google.generativeai as genai

# 🔑 API KEY (yahan apni NEW ke)
genai.configure(api_key="AIzaSyC-8EPcF_g-ACRl9oQhcv1rK16cA_syw4Y")

# 🤖 Model
model = genai.GenerativeModel("gemini-2.5-flash")

def generate_guidance(user_input, career, missing_skills):
    prompt = f"""
You are an expert career advisor.

User Skills:
{user_input}

Target Career:
{career}

Missing Skills:
{", ".join(missing_skills)}

Provide response in this format:

1. Personalized Analysis:
   - Strengths
   - Weaknesses

2. Roadmap (Beginner → Advanced):
   - Step 1
   - Step 2
   - Step 3

3. Projects (3):
   - Project 1 (Tech stack)
   - Project 2 (Tech stack)
   - Project 3 (Tech stack)

4. Time Estimate:
   - Total time required
"""

    response = model.generate_content(prompt)
    return response.text


