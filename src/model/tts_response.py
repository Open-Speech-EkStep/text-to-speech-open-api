from typing import List

from pydantic import BaseModel


class AudioFile(BaseModel):
    audioContent: str


class AudioConfig(BaseModel):
    language: str
    audioFormat: str = 'wav'
    encoding: str = 'base64'
    samplingRate: int = 22050


class TTSResponse(BaseModel):
    audio: List[AudioFile]
    config: AudioConfig


class TTSFailureResponse(BaseModel):
    status: str = 'ERROR'
    status_text: str
