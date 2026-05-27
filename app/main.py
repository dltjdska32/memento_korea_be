from fastapi import FastAPI

from app.common.exception.exception_handler import register_exception_handlers

app = FastAPI()

register_exception_handlers(app)

