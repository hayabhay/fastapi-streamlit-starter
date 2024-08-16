from config import ENV, LOGGER
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    # Emit a structured log event in production
    if ENV["MODE"] == "prod":
        LOGGER.log_struct(
            {
                "item_id": item_id,
                "q": q,
            },
            severity="INFO",
        )

    return {"item_id": item_id, "q": q}
