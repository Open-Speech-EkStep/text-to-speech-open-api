import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings
from src.routers import tts_routes
from src import log_setup

LOGGER = log_setup.get_logger(__name__)

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
    LOGGER.info(f'Loading with settings {settings}')
    uvicorn.run(
        "server:app", host="0.0.0.0", port=settings.server_port, log_level=settings.log_level.lower(), reload=False
    )
