from fastapi import APIRouter
from fastapi import Response, status

from src import log_setup
from src.application.tts_preprocess import infer_tts_request
from src.model.tts_request import TTSRequest
from src.model.tts_response import TTSFailureResponse

LOGGER = log_setup.get_logger(__name__)
router = APIRouter()


@router.post("/")
async def tts(request: TTSRequest, response: Response):
    LOGGER.info(f'TTS request {request}')
    try:
        infer_response = infer_tts_request(request)
        return infer_response
    except Exception as e:
        LOGGER.exception('Failed to infer %s', e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return TTSFailureResponse(status_text=f'Failed to process request {str(e)}')
