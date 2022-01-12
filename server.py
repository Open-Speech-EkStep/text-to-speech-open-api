import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers import tts_routes

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tts_routes.router)

if __name__ == "__main__":
    uvicorn.run(
        "server:app", host="0.0.0.0", port=5000, log_level="info", reload=True
    )
