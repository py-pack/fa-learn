from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from core.models import Base, db_helper
from api_v1 import router as router_v1
from item_views import router as items_router
from users.views import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    async with db_helper.engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield
    # Clean up the ML models and release the resources


app = FastAPI(lifespan=lifespan)

app.include_router(items_router, tags=["Items"])
app.include_router(user_router, tags=["Users"])
app.include_router(router_v1)


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
