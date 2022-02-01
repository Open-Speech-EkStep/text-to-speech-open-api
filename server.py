import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from src import log_setup
from src.config import settings
from src.routers import tts_routes
from src.routers.exception_handler import validation_exception_handler

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
app.add_exception_handler(RequestValidationError, validation_exception_handler)

if __name__ == "__main__":
    LOGGER.info(f'Loading with settings {settings}')
    uvicorn.run(
        "server:app", host="0.0.0.0", port=settings.server_port, log_level=settings.log_level.lower(), reload=False
    )
