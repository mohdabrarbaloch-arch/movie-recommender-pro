from fastapi import FastAPI
from app import crud, recommender
from app.database import engine
from app.models import Base
from app.ml_model import recommend_movies

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "API Running 🚀"}

@app.get("/add-data")
def add_data():
    return crud.add_dummy_items()

@app.get("/items")
def items():
    return crud.get_items()

@app.get("/interact")
def interact(user_id: int, item_id: int, action: str):
    return crud.add_interaction(user_id, item_id, action)

@app.get("/hybrid-recommend/{user_id}")
def hybrid(user_id: int):
    return recommender.hybrid_recommend(user_id)


@app.get("/search")
def search(movie: str):
    from app.ml_model import recommend_movies

    try:
        results = list(recommend_movies(movie).keys())
        clean = [m.split(" (")[0] for m in results]
        return clean
    except:
        return []