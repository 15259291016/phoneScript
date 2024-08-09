from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from commander.app.models.item import Item
from commander.app.schemas.item import ItemCreate, ItemResponse
from commander.app.db.session import get_db

router = APIRouter()

@router.post("/items/", response_model=ItemResponse)
def create_item(item_in: ItemCreate, db: Session = Depends(get_db)):
    db_item = Item(**item_in.dict())  # 使用 Pydantic 模型的数据创建 ORM 实例
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/items/{item_id}", response_model=ItemResponse)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item
