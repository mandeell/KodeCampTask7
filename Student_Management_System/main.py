from fastapi import FastAPI
from .utils import create_db_and_tables

app = FastAPI()

app.include_router()