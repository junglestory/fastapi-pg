from fastapi import FastAPI
from fastapi.params import Depends 
from sqlalchemy.orm import Session
from db.connection import get_db
from pydantic import ValidationError
from models import Board
import schemas

def Response(status, message, data):
    return {
        "status": status,
        "message": message,
        "data": data
    }

app = FastAPI()

@app.get("/") 
def hello(): 
    return {"Hello": "World"}


@app.post("/board")
def create_news(item: schemas.Item, db: Session = Depends(get_db)):
    try:
        board = Board()
        board.journal_id = item.journal_id
        board.title =  item.title
        board.publish_date =  item.publish_date
        board.link_url =  item.link_url
        board.writer =  item.writer
        board.content =  item.content
        
        db.add(board)
        db.flush()

        db.refresh(board, attribute_names=['board_no'])
        data = {"board_no": board.board_no}
        db.commit()

        status = True
        message = "Board added successfully."
    except ValidationError as e:
        status = False
        data = None
        message = e
    
    return Response(status, message, data)