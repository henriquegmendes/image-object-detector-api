from fastapi import FastAPI

import process.routes
from handlers.error_handler import InitExceptionHandlerMiddleware
from pkg import get_yolo_opencv as init_yolo_opencv
from settings import settings

app = FastAPI(title="Image Object Detector API", description="An Experiment using Python with Yolo and OpenCV", version="1.0.0")

routes = [
    process.routes.routes,
]


@app.on_event("startup")
async def startup():
    init_yolo_opencv()
    InitExceptionHandlerMiddleware(app)

    for route in routes:
        app.include_router(route)
