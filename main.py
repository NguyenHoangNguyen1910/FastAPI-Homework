from fastapi import FastAPI, Depends 
from pydantic import BaseModel, field_validator, model_validator
import sqlite3 as sql
from contextlib import asynccontextmanager
import random 
from fastapi.middleware.cors import CORSMiddleware


DATABASE = "todos.db"


def add_random_todos(): # Đoạn này là dùng AI thêm vào do lười nghĩ data
    conne = sql.connect(DATABASE)

    Titles = [
        "Hoc FastAPI",
        "Lam bai tap",
        "Hoc SQLite",
        "Doc tai lieu",
        "Lam project"
    ]

    Descriptions = [
        "Hoc vao buoi sang",
        "Lam truoc deadline",
        "Can hoan thanh som",
        None
    ]

    for i in range(5):
        Title = Titles[i]
        Description = random.choice(Descriptions)
        Priority = random.randint(1, 5)
        Completed = random.choice([True, False])

        conne.execute(
            """
            INSERT INTO todos (Title, description, priority, completed)
            VALUES (?, ?, ?, ?)
            """,
            (
                Title,
                Description,
                Priority,
                Completed
            )
        )

    conne.commit()
    conne.close()
    
    
def create_db():
    conne = sql.connect(DATABASE)
    conne.execute("""
        CREATE TABLE IF NOT EXISTS ToDos(
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Title TEXT NOT NULL,
            Description TEXT,
            Priority INTEGER NOT NULL,
            Completed INTEGER NOT NULL
        )
                  """)
    
    conne.commit()
    conne.close()
    

@asynccontextmanager 
async def lifespan(app: FastAPI): 
    create_db()
    #add_random_todos()
    yield 
    
    print("DAng tat nguon ung dung")
    
app = FastAPI(lifespan = lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)


def get_db():
    conne = sql.connect(DATABASE)
    conne.row_factory = sql.Row
    try :
        yield conne
    finally : 
        conne.close()


class ToDoCreate(BaseModel):
    Title : str
    Description: str | None = None
    Priority: int = 1
    Completed: bool = False
    
    @field_validator("Title")
    @classmethod
    def validate_title(cls, value: str):
        if not value.strip():
            raise ValueError("Title khong duoc de trong")
        return value.strip()
    
    @model_validator(mode="after") # 
    def validate_priority(self):
        if self.Priority >= 4 and not self.Description : 
            raise ValueError("description bat buoc phai co khi Priority > 4")
        return self
    
    
@app.get("/")
def root():
    return {"message": "Hello fastapi"}


@app.post("/todos")
def create_todo(todo : ToDoCreate, db = Depends(get_db)):
    db.execute(
        """
        insert into ToDos(Title, Description, Priority, Completed)
        values(?, ?, ?, ?) 
        
        """,
        (
        todo.Title, 
        todo.Description, 
        todo.Priority, 
        todo.Completed
         )
    )
    db.commit()
    return {"message":"Cretae sucessully"}


@app.get("/todos")
def get_todos(db=Depends(get_db)):
    rows = db.execute(
        "select * from ToDos"
    ).fetchall()
    
    result = []
    for row in rows :
        result.append(dict(row))
    return result
    

@app.get("/todos/{todo_id}")
def get_todo(todo_id: int, db = Depends(get_db)):
    row = db.execute(
        "select * from ToDos where Id  = ?",
        (todo_id,)
    ).fetchone()
    
    if row == None :
        return {"message": "Todo not found"}
    
    return dict(row)


@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, todo : ToDoCreate, db = Depends(get_db)):
    
    row = db.execute(
        "select * from ToDos where Id  = ?",
        (todo_id,)
    ).fetchone()
    
    if row == None :
        return {"message": "Todo not found"}
    
    db.execute(
        """
        update ToDos
        set Title = ?, Description = ?, Priority = ?, Completed = ?
        where Id  = ?
        """,
        (
            todo.Title,
            todo.Description,
            todo.Priority,
            todo.Completed,
            todo_id
        )
    )
    
    db.commit()
    
    return {"message": "Updated successfully"}


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db = Depends(get_db)):
    
    row = db.execute(
        "select * from ToDos where Id  = ?",
        (todo_id,)
    ).fetchone()
    
    if row == None :
        return {"message": "Todo not found"}
    
    db.execute(
        "delete from ToDos where Id  = ?",
        (todo_id,)
    )
    
    db.commit()
    
    return {"message": "Deleted successfully"}


@app.get("/health/live") # liveliness
def liveness():
    return {"status": "alive"}


@app.get("/health/ready") #readiness
def readiness(db=Depends(get_db)):
    db.execute("SELECT 1")
    return {"status": "ready"}