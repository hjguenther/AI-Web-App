from sqlalchemy.orm import Session
from .models import Item

def get_items(db: Session):
    return db.query(Item).all()

def create_item(db: Session, name: str):
    item = Item(name=name)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
