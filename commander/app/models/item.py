from sqlalchemy import Column, Integer, String, Float, Text
from commander.app.db.base_class import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    tax = Column(Float, nullable=True)
