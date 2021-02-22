from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from data import munge

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return munge()
