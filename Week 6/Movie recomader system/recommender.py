import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
new_movies = pd.read_csv(
    "data/netflix_movies_cleaned.csv"
)

my_tfidf = TfidfVectorizer(
    stop_words="english"
)

my_tfidf_mat=my_tfidf.fit_transform(new_movies["combined_features"])
mat_similarity = cosine_similarity(my_tfidf_mat)
movie_idx = pd.Series(
    new_movies.index,
    index=new_movies["title"]
).drop_duplicates()

def my_movie_recomnander(title, num_recommendations=10):

    if title not in movie_idx:
        return []

    idx = movie_idx[title]

    my_similarity_scores = list(
        enumerate(mat_similarity[idx])
    )

    my_similarity_scores = sorted(
        my_similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )

    my_similarity_scores = my_similarity_scores[
        1:num_recommendations + 1
    ]

    recommendations = []

    for movie_index, score in my_similarity_scores:

        movie = new_movies.iloc[movie_index]

        recommendations.append({
            "title": movie["title"],
            "release_year": int(movie["release_year"]),
            "rating": movie["rating"],
            "duration": movie["duration"],
            "genre": movie["listed_in"],
            "description": movie["description"],
            "similarity": round(float(score), 4)
        })

    return recommendations

if __name__ == "__main__":

    recommendations = my_movie_recomnander(
        "Inception",
        5
    )

    for movie in recommendations:
        print(movie)