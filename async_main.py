from fastapi import FastAPI, Depends
from pydantic import BaseModel, field_validator, model_validator
from contextlib import asynccontextmanager
import random
from fastapi.middleware.cors import CORSMiddleware
import aiosqlite
import time 


DATABASE = "todos_async.db"


async def add_random_todos():
    conne = await aiosqlite.connect(DATABASE)

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

        await conne.execute(
            """
            INSERT INTO ToDos (Title, Description, Priority, Completed)
            VALUES (?, ?, ?, ?)
            """,
            (
                Title,
                Description,
                Priority,
                Completed
            )
        )

    await conne.commit()
    await conne.close()


async def create_db():
    conne = await aiosqlite.connect(DATABASE)

    await conne.execute(
        """
        CREATE TABLE IF NOT EXISTS ToDos(
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Title TEXT NOT NULL,
            Description TEXT,
            Priority INTEGER NOT NULL,
            Completed INTEGER NOT NULL
        )
        """
    )

    await conne.commit()
    await conne.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db()

    # await add_random_todos()

    yield

    print("Dang tat nguon ung dung")


app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)


async def get_db():
    conne = await aiosqlite.connect(DATABASE)

    conne.row_factory = aiosqlite.Row

    try:
        yield conne

    finally:
        await conne.close()


class ToDoCreate(BaseModel):
    Title: str
    Description: str | None = None
    Priority: int = 1
    Completed: bool = False

    @field_validator("Title")
    @classmethod
    def validate_title(cls, value: str):
        if not value.strip():
            raise ValueError("Title khong duoc de trong")

        return value.strip()

    @model_validator(mode="after")
    def validate_priority(self):
        if self.Priority >= 4 and not self.Description:
            raise ValueError(
                "description bat buoc phai co khi Priority >= 4"
            )

        return self


@app.get("/")
async def root():
    return {"message": "Hello fastapi async"}


@app.post("/todos")
async def create_todo(
    todo: ToDoCreate,
    db=Depends(get_db)
):
    await db.execute(
        """
        INSERT INTO ToDos(Title, Description, Priority, Completed)
        VALUES (?, ?, ?, ?)
        """,
        (
            todo.Title,
            todo.Description,
            todo.Priority,
            todo.Completed
        )
    )

    await db.commit()

    return {"message": "Create successfully"}


@app.get("/todos")
async def get_todos(
    db=Depends(get_db)
):
    cursor = await db.execute(
        "SELECT * FROM ToDos"
    )

    rows = await cursor.fetchall()

    result = []

    for row in rows:
        result.append(dict(row))

    return result


@app.get("/todos/{todo_id}")
async def get_todo(
    todo_id: int,
    db=Depends(get_db)
):
    cursor = await db.execute(
        "SELECT * FROM ToDos WHERE Id = ?",
        (todo_id,)
    )

    row = await cursor.fetchone()

    if row is None:
        return {"message": "Todo not found"}

    return dict(row)


@app.put("/todos/{todo_id}")
async def update_todo(
    todo_id: int,
    todo: ToDoCreate,
    db=Depends(get_db)
):

    cursor = await db.execute(
        "SELECT * FROM ToDos WHERE Id = ?",
        (todo_id,)
    )

    row = await cursor.fetchone()

    if row is None:
        return {"message": "Todo not found"}

    await db.execute(
        """
        UPDATE ToDos
        SET Title = ?,
            Description = ?,
            Priority = ?,
            Completed = ?
        WHERE Id = ?
        """,
        (
            todo.Title,
            todo.Description,
            todo.Priority,
            todo.Completed,
            todo_id
        )
    )

    await db.commit()

    return {"message": "Updated successfully"}


@app.delete("/todos/{todo_id}")
async def delete_todo(
    todo_id: int,
    db=Depends(get_db)
):

    cursor = await db.execute(
        "SELECT * FROM ToDos WHERE Id = ?",
        (todo_id,)
    )

    row = await cursor.fetchone()

    if row is None:
        return {"message": "Todo not found"}

    await db.execute(
        "DELETE FROM ToDos WHERE Id = ?",
        (todo_id,)
    )

    await db.commit()

    return {"message": "Deleted successfully"}


@app.get("/health/live")
async def liveness():
    return {"status": "alive"}


@app.get("/health/ready")
async def readiness(
    db=Depends(get_db)
):
    await db.execute("SELECT 1")

    return {"status": "ready"}

