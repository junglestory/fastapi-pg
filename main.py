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


@app.get("/board")
def get_board_all(db: Session = Depends(get_db)):
    datas = db.query(Board).all()

    status = True
    message = "Board retrieved successfully"

    if len(datas) <= 0:
        status = False
        message = "Board not found"
    
    return Response(status, message, datas)


@app.get("/board/{board_no}")
def get_board_by_board_no(board_no: str, db: Session = Depends(get_db)):
    datas = db.query(Board).filter(Board.board_no == board_no).all()

    status = True
    message = "Board retrieved successfully"

    if len(datas) <= 0:
        status = False
        message = "Board not found"

    return Response(status, message, datas)


@app.post("/board")
def create_board(item: schemas.Item, db: Session = Depends(get_db)):
    try:
        board = Board()
        board.title =  item.title
        board.contents =  item.contents
        board.writer =  item.writer        
        board.view_count =  item.view_count
        board.link_url =  item.link_url
        
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


@app.put("/board")
def update_board(item: schemas.Item, db: Session = Depends(get_db)):
    try:
        is_updated = db.query(Board).filter(Board.board_no == item.board_no).update({
            Board.title: item.title,
            Board.contents: item.contents,
            Board.writer: item.writer,
            Board.view_count: item.view_count,
            Board.link_url: item.link_url            
        }, synchronize_session=False)
        
        db.flush()
        db.commit()

        status = True
        message = "Board updated successfully"        
        
        if is_updated == 1:
            data = db.query(Board).filter(Board.board_no == item.board_no).one()
        elif is_updated == 0:
            message = "Board not updated. No product found with this board_no :" + \
                str(item.board_no)
            status = False
            data = None        
    except Exception as e:
        status = False
        data = None
        message = e

    return Response(status, message, data)


@app.delete("/board/{board_no}")
def delete_board(board_no: int, db: Session = Depends(get_db)):
    data = None

    try:
        status = True
        
        is_deleted = db.query(Board).filter(Board.board_no == board_no).delete()
        db.commit()

        if is_deleted == 1:
            message = "Board deleted successfully"
        else:
            message = "Board not updated. No product found with this board_no :" + \
                str(board_no)    
    except Exception as e:
        status = False
        message = e

    return Response(status, message, data)