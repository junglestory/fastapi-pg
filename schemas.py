from pydantic import BaseModel

class Item(BaseModel):
    board_no: int | None = None
    title: str
    contents: str
    writer: str | None = None
    view_count: int | None = None
    link_url: str | None = None

    class Config:
        orm_mode = True