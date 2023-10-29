from fastapi import FastAPI
import uvicorn

from item_views import router as items_router
from users.views import router as user_router

app = FastAPI()

app.include_router(items_router, tags=["Items"])
app.include_router(user_router, tags=["Users"])


@app.get("/")
def hello_index():
    return {"message": "Hello index!"}


@app.get("/hello/")
def hello(name: str = "Suren"):
    name = name.strip().title()
    return {"message": f"Hello {name}"}


@app.post("/calc/add")
def calc_add(a: int, b: int):
    return {"a": a, "b": b, "result": a + b}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
