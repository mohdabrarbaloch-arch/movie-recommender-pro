from app import crud
from app.ml_model import recommend_movies, similarity_df

def hybrid_recommend(user_id):
    interactions = crud.get_user_interactions(user_id)

    if not interactions:
        return {"message": "No user data"}

    all_recommendations = []

    for item in interactions:
        try:
            movie = crud.get_item_by_id(item.item_id)

            if not movie:
                continue

            # ✅ clean DB title
            movie_name = movie.title.strip()

            # ✅ smart match with dataset
            matches = [m for m in similarity_df.columns if movie_name.lower() in m.lower()]

            if not matches:
                continue

            movie_name = matches[0]

            # ✅ get recommendations
            recs = recommend_movies(movie_name)

            if isinstance(recs, dict) and "error" in recs:
                continue

            all_recommendations.extend(list(recs.keys()))

        except Exception as e:
            print("Error:", e)
            continue

    # ✅ remove duplicates
    unique = list(set(all_recommendations))

    # ✅ clean names (remove year)
    clean = [m.split(" (")[0] for m in unique]

    return clean[:5]