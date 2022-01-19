from typing import List

from pydantic import BaseModel

from src.model.language import Language


class Sentence(BaseModel):
    source: str


class TTSConfig(BaseModel):
    language: Language
    gender: str


class TTSRequest(BaseModel):
    input: List[Sentence]
    config: TTSConfig

# TODO: Add validation for possible values of gender and language
