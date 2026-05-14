



from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def jd_match(user_input, job_desc):
    texts = [user_input, job_desc]

    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(texts)

    similarity = cosine_similarity(tfidf[0], tfidf[1])[0][0]

    return round(similarity * 100, 2)
