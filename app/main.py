from fastapi import FastAPI
from app.routers import credit_score

app = FastAPI()

app.include_router(credit_score.router)