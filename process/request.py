from pydantic import BaseModel


class ProcessImageRequest(BaseModel):
    external_id: str
    image_url: str = ''
    file_extension: str = 'jpg'
    threshold: float = 0.5
