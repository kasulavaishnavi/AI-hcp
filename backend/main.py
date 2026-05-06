from fastapi import FastAPI
from routes.agent_route import router
from db.connection import init_db

app = FastAPI()
init_db()

app.include_router(router)

@app.get("/")
def home():
    return {"message": "AI CRM Backend Running"}

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)