from fastapi import FastAPI
from spbd.routers.v1.user import user_router

app = FastAPI()
app.include_router(user_router)


@app.get('/version')
def version():
    return {'version': '0.1.0'}
