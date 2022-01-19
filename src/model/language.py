from pydantic import BaseModel


class Language(BaseModel):
    sourceLanguage: str
