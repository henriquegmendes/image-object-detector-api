import logging

from fastapi import Request
from fastapi.responses import JSONResponse

from process.errors import GenericException


class InitExceptionHandlerMiddleware:
    def __init__(self, app):
        @app.exception_handler(GenericException)
        async def generic_exception_handler(request: Request, exc):
            logging.error(exc.message)
            return JSONResponse(
                status_code=409,
                content={"message": exc.message},
            )

        @app.exception_handler(Exception)
        async def default_exception_handler(request: Request, exc):
            logging.error(exc)
            return JSONResponse(
                status_code=500,
                content={"message": 'Unexpected error'},
            )
