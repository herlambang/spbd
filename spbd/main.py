import logging
import logging.config
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from spbd import utils
from spbd.core import loggs
from spbd.core.config import settings
from spbd.routers.v1.audio import audio_router
from spbd.routers.v1.user import user_router

log_config = loggs.LOGGING if settings.env_ == "dev" else loggs.LOGGING_PRODUCTION
logging.config.dictConfig(log_config)
log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ensure directory creation
    print(settings.env_)
    utils.get_cached_dir()
    utils.get_audio_dir()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(user_router)
app.include_router(audio_router)


@app.get("/version")
def version():
    return {"version": "0.1.0"}


@app.exception_handler(500)
async def internal_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder({"detail": "Internal Server Error"}),
    )
