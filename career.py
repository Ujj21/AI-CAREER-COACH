from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# 🔍 Career match (already tha)
def get_career_matches(data, user_input):
    all_skills = data["Skills"].tolist()
    all_skills.append(user_input)

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(all_skills)

    user_vector = tfidf_matrix[-1]
    career_vector = tfidf_matrix[:-1]

    similarity_score = cosine_similarity(user_vector, career_vector)

    data["Similarity Score"] = similarity_score.flatten()
    data = data.sort_values(by="Similarity Score", ascending=False)

    return data.head(3)


def get_missing_skills(user_input, career_skills):
    user_skills = set([skill.strip().lower() for skill in user_input.split(",")])
    career_skills = set([skill.strip().lower() for skill in career_skills.split(",")])

    missing = career_skills - user_skills
    return list(missing)
