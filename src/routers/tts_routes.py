from fastapi import APIRouter

from src.application.tts_preprocess import infer_tts
from src.config import settings
from src.model.tts_request import TTSRequest

router = APIRouter()


@router.post("/TTS/")
async def tts(request: TTSRequest):
    encoded_string, sr = infer_tts(request)
    print('request', request)
    print('settings', settings)
    return {"encoding": "base64", "data": encoded_string, "sr": sr}
