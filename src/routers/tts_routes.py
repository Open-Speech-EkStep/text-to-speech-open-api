from fastapi import APIRouter

from src import log_setup
from src.application.tts_preprocess import infer_tts
from src.model.tts_request import TTSRequest

LOGGER = log_setup.get_logger(__name__)
router = APIRouter()


@router.post("/TTS/")
async def tts(request: TTSRequest):
    LOGGER.info(f'TTS request {request}')
    try:
        response = infer_tts(request)
    except Exception as e:
        LOGGER.exception('Failed to infer %s', e)

    if response is not None:
        return response
    else:
        return {"error": 'Failed to process: ' + str(e)}
