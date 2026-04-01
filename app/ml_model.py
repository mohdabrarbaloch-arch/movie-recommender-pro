import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

movies = pd.read_csv(os.path.join(BASE_DIR, "movies.csv"))
ratings = pd.read_csv(os.path.join(BASE_DIR, "ratings.csv"))

data = pd.merge(ratings, movies, on="movieId")

pivot = data.pivot_table(index="title", columns="userId", values="rating").fillna(0)

similarity = cosine_similarity(pivot)
similarity_df = pd.DataFrame(similarity, index=pivot.index, columns=pivot.index)

def recommend_movies(movie_name):
    if movie_name not in similarity_df.columns:
        return {}

    similar = similarity_df[movie_name].sort_values(ascending=False)
    return similar[1:6]