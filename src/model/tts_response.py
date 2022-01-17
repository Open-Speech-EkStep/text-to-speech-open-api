from pydantic import BaseModel


class TTSResponse(BaseModel):
    data: str
    sr: str
    encoding: str = 'base64'
