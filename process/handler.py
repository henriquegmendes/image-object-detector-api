from fastapi.responses import FileResponse

from . import request, service


async def process(req: request.ProcessImageRequest) -> dict:
    return await service.process_image(req, 0.3)


def static_result_file_by_id(process_id: str):
    path, mime_type = service.static_file_by_path(process_id)
    return FileResponse(path, media_type=mime_type)
