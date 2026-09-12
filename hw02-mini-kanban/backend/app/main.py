"""Small, persistent task board API."""

import os
from datetime import datetime, timezone
from typing import Literal

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import DateTime, Integer, String, Text, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker


Status = Literal["todo", "doing", "done"]


class Base(DeclarativeBase):
    pass


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(10), default="todo")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class NewTask(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str = Field(default="", max_length=500)


class MoveTask(BaseModel):
    status: Status


class TaskOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    status: Status
    created_at: datetime


def create_app(database_url: str | None = None) -> FastAPI:
    database_url = database_url or os.getenv("TASKLANE_DATABASE_URL", "sqlite:///./tasklane.sqlite3")
    engine = create_engine(database_url, connect_args={"check_same_thread": False} if database_url.startswith("sqlite") else {})
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(engine, expire_on_commit=False)
    app = FastAPI(title="TaskLane API")
    app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], allow_methods=["*"], allow_headers=["*"])

    def get_db():
        with session_factory() as db:
            yield db

    @app.get("/api/tasks", response_model=list[TaskOut])
    def list_tasks(db: Session = Depends(get_db)):
        return db.scalars(select(Task).order_by(Task.created_at, Task.id)).all()

    @app.post("/api/tasks", response_model=TaskOut, status_code=201)
    def create_task(data: NewTask, db: Session = Depends(get_db)):
        title = data.title.strip()
        if not title:
            raise HTTPException(422, "Title cannot be blank")
        task = Task(title=title, description=data.description.strip())
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    @app.patch("/api/tasks/{task_id}", response_model=TaskOut)
    def move_task(task_id: int, data: MoveTask, db: Session = Depends(get_db)):
        task = db.get(Task, task_id)
        if task is None:
            raise HTTPException(404, "Task not found")
        task.status = data.status
        db.commit()
        db.refresh(task)
        return task

    @app.delete("/api/tasks/{task_id}", status_code=204)
    def delete_task(task_id: int, db: Session = Depends(get_db)):
        task = db.get(Task, task_id)
        if task is None:
            raise HTTPException(404, "Task not found")
        db.delete(task)
        db.commit()

    return app


app = create_app()

