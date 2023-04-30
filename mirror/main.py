from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"]
)

app.include_router(router)