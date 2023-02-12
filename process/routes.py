from fastapi import APIRouter
from fastapi.responses import FileResponse

from . import request, handler

routes = APIRouter(tags=['images'], prefix='/api/v1/images')


@routes.post('', description='Create and process a new image request', status_code=200, response_model=dict)
async def create(req: request.ProcessImageRequest) -> dict:
    return await handler.process(req)


@routes.get('/results/{process_id}', description='Returns processed file by process id', response_class=FileResponse)
def serve_result_file(process_id: str):
    return handler.static_result_file_by_id(process_id)
