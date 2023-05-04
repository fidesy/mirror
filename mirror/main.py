from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://mirror.fidesy.xyz"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"]
)

app.include_router(router)