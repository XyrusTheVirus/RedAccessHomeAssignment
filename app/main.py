from fastapi import FastAPI
from api.routes import api_router
import logging
import os

logging.basicConfig(level=logging.getLevelName(os.getenv("LOG_LEVEL", "INFO")))
app = FastAPI(redirect_slashes=False)
app.include_router(api_router)
