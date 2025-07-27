from fastapi import FastAPI, HTTPException, status, Response
from models.db import db
from models.models import Sheep
from pydantic import BaseModel
from typing import List

app = FastAPI()

@app.get("/sheep/{id}", response_model=Sheep)
def read_sheep(id: int):
    return db.get_sheep(id)

@app.post("/sheep/", response_model=Sheep, status_code=status.HTTP_201_CREATED)
def add_sheep(sheep: Sheep):
    if sheep.id in db.data:
        raise HTTPException(status_code=400, detail="Sheep with this ID already exists")

    db.data[sheep.id] = sheep
    return sheep

@app.delete("/sheep/{id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_sheep(id: int):
    try:
        db.delete_sheep(id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Sheep not found")
    return Response(status_code=204)

class SheepUpdate(BaseModel):
    name: str
    breed: str
    sex: str

@app.put("/sheep/{id}", response_model=Sheep)
def update_sheep(id: int, sheep_update: SheepUpdate):
    try:
        updated_sheep = db.update_sheep(id, sheep_update.model_dump(exclude_unset=True))
        return updated_sheep
    except ValueError:
        raise HTTPException(status_code=404, detail="Sheep not found")

@app.get("/sheep/", response_model=List[Sheep])
def read_all_sheep():
    return db.get_all_sheep()
