from sqlalchemy import Column, String, Integer, TEXT, DATETIME
from db.database import Base
from sqlalchemy.sql import func

class Board(Base):
    __tablename__ = "board"

    board_no = Column(Integer, primary_key=True, index=True)  
    title = Column(String(200))
    contents = Column(TEXT)
    writer = Column(String(50))
    view_count = Column(Integer)
    link_url = Column(String(200))
    create_date = Column(DATETIME(timezone=True), server_default=func.now())
    update_date = Column(DATETIME(timezone=True), server_default=func.now())