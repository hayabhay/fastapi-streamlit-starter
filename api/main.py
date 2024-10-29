from functools import lru_cache
from config import Settings
from fastapi import FastAPI

@lru_cache
def get_settings():
    return Settings()

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
