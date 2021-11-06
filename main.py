from typing import Optional, Literal

from fastapi import FastAPI
from pydantic import BaseModel, Json, ValidationError
from pydantic.utils import Obj


def create_area(area):
    return area



class WebhookJsonModel(BaseModel):
    event: str
    timestamp: str
    model: str
    username: str
    request_id: str
    data: Obj
    snapshots: Obj

class WebhookResponseModel(BaseModel):
    message: Literal["Received site webhook from Netbox"]
    data: WebhookJsonModel

app = FastAPI()

# base test endpoint
@app.get("/")
async def root():
    return {"message": "Hello World"}

#sites endpoint
@app.post("/sites/", response_model=WebhookResponseModel)
def sites(site_data: WebhookJsonModel):
    create_area(site_data.data)
    return {
        "message": "Received site webhook from Netbox",
        "data": site_data
    }