from fastapi import FastAPI
from cart.web.router import router


def create_application():
    client = FastAPI()
    client.include_router(router)
    return client

app = create_application()
