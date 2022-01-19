from typing import List

from pydantic import BaseModel


class Sentence(BaseModel):
    source: str


class Language(BaseModel):
    sourceLanguage: str


class TTSConfig(BaseModel):
    language: Language
    gender: str


class TTSRequest(BaseModel):
    input: List[Sentence]
    config: TTSConfig

# TODO: Add validation for possible values of gender and language
