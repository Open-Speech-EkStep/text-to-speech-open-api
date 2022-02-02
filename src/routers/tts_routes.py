from fastapi import APIRouter

from src import log_setup
from src.application.tts_preprocess import infer_tts_request
from src.model.tts_request import TTSRequest
from src.model.tts_response import TTSFailureResponse

LOGGER = log_setup.get_logger(__name__)
router = APIRouter()


@router.post("/")
async def tts(request: TTSRequest):
    LOGGER.info(f'TTS request {request}')
    response = None
    error = None
    try:
        response = infer_tts_request(request)
    except Exception as e:
        LOGGER.exception('Failed to infer %s', e)
        error = e
    if response is not None:
        return response
    else:
        return TTSFailureResponse(status_text=f'Failed to process request {str(error)}')
