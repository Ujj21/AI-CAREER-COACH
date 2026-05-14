import streamlit as st
import pandas as pd

from career import get_career_matches, get_missing_skills
from resume import chat_with_resume
from llm import generate_guidance
from jd_matcher import jd_match
from resume_analyzer import extract_text_from_pdf, analyze_resume

# =========================
# 🎨 PAGE CONFIG
# =========================
st.set_page_config(
    page_title="AI Career Coach",
    page_icon="🚀",
    layout="wide"
)

# =========================
# 🎨 CUSTOM CSS
# =========================
st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

h1, h2, h3 {
    color: white;
}

.stButton > button {
    width: 100%;
    border-radius: 10px;
    height: 3em;
    font-size: 16px;
    font-weight: bold;
}

.stTextInput > div > div > input {
    border-radius: 10px;
}

.stTextArea textarea {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# 📌 SIDEBAR
# =========================
st.sidebar.title("📌 Features")

option = st.sidebar.radio(
    "Choose Feature",
    [
        "Home",
        "Resume Chat",
        "Skill Roadmap",
        "JD Match",
        "Resume Analyzer"
    ]
)

# =========================
# 🏠 HOME PAGE
# =========================
if option == "Home":

    st.markdown("""
    <div style='text-align: center; padding: 100px 30px;'>

    <h1 style='font-size: 65px; font-weight: bold;'>
    🚀 AI Career Coach
    </h1>

    <h3 style='color: gray; font-weight: normal;'>
    Your AI-powered Resume & Career Assistant
    </h3>

    </div>
    """, unsafe_allow_html=True)

# =========================
# 📄 RESUME CHAT
# =========================
elif option == "Resume Chat":

    st.title("📄 Resume Chat Assistant")

    uploaded_file = st.file_uploader(
        "Upload Resume (PDF)",
        type=["pdf"]
    )

    if uploaded_file:

        resume_text = extract_text_from_pdf(uploaded_file)

        st.success("✅ Resume Uploaded Successfully")

        question = st.text_input(
            "Ask something about your resume"
        )

        if st.button("Ask AI"):

            with st.spinner("Thinking..."):

                answer = chat_with_resume(
                    resume_text,
                    question
                )

            st.subheader("🤖 AI Response")

            st.write(answer)

# =========================
# 📊 SKILL ROADMAP
# =========================
elif option == "Skill Roadmap":

    st.title("📊 Career Guidance")

    data = pd.read_csv("careers.csv")

    user_input = st.text_input(
        "Enter your skills (comma separated)"
    )

    if st.button("Generate Roadmap"):

        with st.spinner("Analyzing skills..."):

            top_matches = get_career_matches(
                data,
                user_input
            )

        st.subheader("🎯 Top Career Matches")

        for i in range(len(top_matches)):

            role = top_matches.iloc[i]["Role"]

            score = round(
                top_matches.iloc[i]["Similarity Score"] * 100,
                2
            )

            st.progress(int(score) / 100)

            st.success(
                f"{i+1}. {role} — {score}% Match"
            )

        best_role = top_matches.iloc[0]["Role"]

        role_skills = top_matches.iloc[0]["Skills"]

        missing_skills = get_missing_skills(
            user_input,
            role_skills
        )

        c1, c2 = st.columns(2)

        with c1:
            st.metric(
                "Best Career Match",
                best_role
            )

        with c2:
            st.metric(
                "Missing Skills",
                len(missing_skills)
            )

        st.subheader("⚠️ Missing Skills")

        if missing_skills:

            for skill in missing_skills:
                st.warning(skill)

        else:
            st.success("No Missing Skills 🎉")

        with st.spinner("Generating roadmap..."):

            result = generate_guidance(
                user_input,
                best_role,
                missing_skills
            )

        st.subheader("🚀 AI Career Roadmap")

        st.info(result)

# =========================
# 📄 JD MATCH
# =========================
elif option == "JD Match":

    st.title("📄 Job Description Match")

    user_input = st.text_area(
        "Enter your skills"
    )

    job_desc = st.text_area(
        "Paste Job Description"
    )

    if st.button("Check Match"):

        score = jd_match(
            user_input,
            job_desc
        )

        st.subheader("🎯 Match Score")

        st.progress(score / 100)

        if score >= 75:
            st.success(f"Excellent Match — {score}%")

        elif score >= 50:
            st.warning(f"Good Match — {score}%")

        else:
            st.error(f"Low Match — {score}%")

# =========================
# 🔍 RESUME ANALYZER
# =========================
elif option == "Resume Analyzer":

    st.title("🔍 AI Resume Analyzer")

    target_role = st.text_input(
        "Target Role (optional)",
        placeholder="e.g. Data Scientist"
    )

    uploaded_file = st.file_uploader(
        "Upload Resume (PDF)",
        type=["pdf"]
    )

    if uploaded_file:

        resume_text = extract_text_from_pdf(
            uploaded_file
        )

        st.success("✅ Resume Loaded Successfully")

        if st.button("Analyze Resume"):

            with st.spinner("Analyzing Resume..."):

                result = analyze_resume(
                    resume_text,
                    target_role
                )

            if result:

                c1, c2, c3, c4 = st.columns(4)

                c1.metric(
                    "ATS Score",
                    f"{result['ats_score']}%"
                )

                c2.metric(
                    "Experience",
                    f"{result['experience_years']} yrs"
                )

                c3.metric(
                    "Skills Found",
                    len(result['skills_found'])
                )

                c4.metric(
                    "Skills Missing",
                    len(result['skills_missing'])
                )

                st.subheader("📈 ATS Score")

                st.progress(
                    result['ats_score'] / 100
                )

                st.subheader("✅ Skills Found")

                for skill in result['skills_found']:
                    st.success(skill)

                st.subheader("⚠️ Missing Skills")

                if result['skills_missing']:

                    for skill in result['skills_missing']:
                        st.warning(skill)

                else:
                    st.success("No Missing Skills 🎉")

                col1, col2 = st.columns(2)

                with col1:

                    st.subheader("💪 Strengths")

                    for s in result['strengths']:
                        st.success(s)

                with col2:

                    st.subheader("🔧 Weaknesses")

                    for w in result['weaknesses']:
                        st.warning(w)

                st.subheader("💡 Improvement Tips")

                st.info(
                    result['improvement_tips']
                )

                with st.expander("📋 Full Analysis"):

                    st.write(
                        result['overall_analysis']
                    )

            else:

                st.error(
                    "Could not analyze resume."
                )