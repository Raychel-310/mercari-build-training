import os
import logging
import pathlib
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
logger = logging.getLogger("uvicorn")
logger.level = logging.INFO
images = pathlib.Path(__file__).parent.resolve() / "images"
origins = [os.environ.get("FRONT_URL", "http://localhost:3000")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# 商品を登録する空のリストを作成
items = []

@app.get("/")
def root():
    return {"message": "Hello, world!"}
# def read_item(item_id: int, q: str = None):
#     if q:
#         return {"item_id": item_id, "q": q}
#     return {"item_id": item_id}


@app.post("/items")
def add_item(name: str = Form(...), category: str = Form(...)):
    item = {"name": name, "category": category}
    items.append(item)
    logger.info(f"Receive item: {name}")
    return {"message": f"item received: {name}"}

@app.get("/items")
def get_items():
    return {"items": items}

@app.get("/image/{image_name}")
async def get_image(image_name):
    # Create image path
    image = images / image_name

    if not image_name.endswith(".jpg"):
        raise HTTPException(status_code=400, detail="Image path does not end with .jpg")

    if not image.exists():
        logger.debug(f"Image not found: {image}")
        image = images / "default.jpg"

    return FileResponse(image)
