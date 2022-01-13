import base64
import io

import numpy as np
import torch
from fastapi import HTTPException
from indicnlp.tokenize import sentence_tokenize
from mosestokenizer import *
from mosestokenizer import *
from scipy.io.wavfile import write
from tts_infer.num_to_word_on_sent import normalize_nums

from src import log_setup
from src.config import settings
from src.infer.model_inference import ModelService
from src.model.tts_request import TTSRequest

LOGGER = log_setup.get_logger(__name__)
model_service = ModelService()
_INDIC = ["as", "bn", "gu", "hi", "kn", "ml", "mr", "or", "pa", "ta", "te"]


def infer_tts(request: TTSRequest):
    lang = request.lang
    gender = request.gender
    text_to_infer = request.text
    choice = lang + "_" + gender
    LOGGER.debug(f'choice for model {choice}')

    if choice in model_service.available_choice.keys():
        t2s = model_service.available_choice[choice]
    else:
        raise HTTPException(
            status_code=400, detail={"error": "Requested model not found"}
        )

    if text_to_infer:
        # text = pre_process_text(text, lang)
        if len(text_to_infer) > settings.tts_max_text_limit:
            LOGGER.debug("Running in paragraph mode...")
            audio, sr = run_tts_paragraph(text_to_infer, lang, t2s)
        else:
            LOGGER.debug("Running in text mode...")
            audio, sr = run_tts(text_to_infer, lang, t2s)
        torch.cuda.empty_cache()
        LOGGER.debug(audio)
        bytes_wav = bytes()
        byte_io = io.BytesIO(bytes_wav)
        write(byte_io, sr, audio)
        encoded_bytes = base64.b64encode(byte_io.read())
        encoded_string = encoded_bytes.decode()
        # write(filename='out.wav', rate=sr, data=audio) #If persisting of files are needed
    else:
        raise HTTPException(status_code=400, detail={"error": "No text"})


def split_sentences(paragraph, language):
    if language == "en":
        with MosesSentenceSplitter(language) as splitter:
            return splitter([paragraph])
    elif language in _INDIC:
        return sentence_tokenize.sentence_split(paragraph, lang=language)


def pre_process_text(text, lang):
    if lang == 'hi':
        text = text.replace('।', '.')  # only for hindi models
    return text


def run_tts_paragraph(text, lang, t2s):
    audio_list = []
    split_sentences_list = split_sentences(text, language='hi')

    for sent in split_sentences_list:
        audio, sr = run_tts(sent, lang, t2s)
        audio_list.append(audio)

    concatenated_audio = np.concatenate([i for i in audio_list])
    # write(filename='temp_long.wav', rate=sr, data=concatenated_audio)
    return concatenated_audio, sr


def run_tts(text, lang, t2s):
    text_num_to_word = normalize_nums(text, lang)  # converting numbers to words in lang
    text_num_to_word_and_transliterated = model_service.transliterate_obj.translit_sentence(text_num_to_word,
                                                                                            lang)  # transliterating english words to lang
    mel = t2s[0].generate_mel(' ' + text_num_to_word_and_transliterated)
    audio, sr = t2s[1].generate_wav(mel)
    return audio, sr
