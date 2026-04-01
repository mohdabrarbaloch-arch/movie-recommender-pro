from app.database import SessionLocal
from app.models import Item, Interaction
from app import models

def add_dummy_items():
    db = SessionLocal()

    items = [
    Item(title="Toy Story (1995)", category="Animation"),
    Item(title="Toy Story 2 (1999)", category="Animation"),
    Item(title="Jurassic Park (1993)", category="Action"),
    Item(title="Independence Day (1996)", category="Sci-Fi"),
    Item(title="Forrest Gump (1994)", category="Drama"),
]

    db.add_all(items)
    db.commit()
    db.close()

    return {"message": "Dummy data added"}


# 🔥 ADD THIS FUNCTION (IMPORTANT)
def add_interaction(user_id: int, item_id: int, action: str):
    db = SessionLocal()

    interaction = Interaction(
        user_id=user_id,
        item_id=item_id,
        action=action
    )

    db.add(interaction)
    db.commit()
    db.close()

    return {"message": "Interaction saved"}


def get_user_interactions(user_id: int):
    db = SessionLocal()
    interactions = db.query(models.Interaction).filter(
        models.Interaction.user_id == user_id
    ).all()
    db.close()
    return interactions


def get_items():
    db = SessionLocal()
    items = db.query(Item).all()
    db.close()
    return items


def get_item_by_id(item_id: int):
    db = SessionLocal()
    item = db.query(Item).filter(Item.id == item_id).first()
    db.close()
    return item