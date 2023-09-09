from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db_api import database
from resources import api_router

app = FastAPI()
app.include_router(api_router)

origins = [
    "http://localhost",
    "https://localohost:4200",
    "https://localohost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
