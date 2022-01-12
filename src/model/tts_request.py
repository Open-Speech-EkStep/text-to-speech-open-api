from typing import Optional

from pydantic import BaseModel


class TTSRequest(BaseModel):
    text: str
    lang: Optional[str] = "hi"
    gender: Optional[str] = "male"
