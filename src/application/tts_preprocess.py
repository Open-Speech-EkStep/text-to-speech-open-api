import base64
import io

import numpy as np
import torch
from fastapi import HTTPException
from indicnlp.tokenize import sentence_tokenize
from mosestokenizer import MosesSentenceSplitter
from scipy.io.wavfile import write
from tts_infer.num_to_word_on_sent import normalize_nums
import nnresample

from src import log_setup
from src.infer.model_inference import ModelService
from src.model.language import Language
from src.model.tts_request import TTSRequest
from src.model.tts_response import TTSResponse, AudioFile, AudioConfig

SAMPLE_RATE = 16000

LOGGER = log_setup.get_logger(__name__)
model_service = ModelService()
_INDIC = ["as", "bn", "gu", "hi", "kn", "ml", "mr", "or", "pa", "ta", "te"]
_PURAM_VIRAM_LANGUAGES = ["hi", "or", "bn", "as"]


def infer_tts_request(request: TTSRequest):
    config = request.config
    lang = config.language.sourceLanguage
    gender = config.gender
    output_list = []
    audio_config = AudioConfig(language=Language(sourceLanguage=lang))
    try:
        for sentence in request.input:
            LOGGER.debug(f'infer for gender {gender} and lang {lang} text {sentence.source}')
            speech_response = infer_tts(language=lang, gender=gender, text_to_infer=sentence.source)
            LOGGER.debug(f'infer done for text {sentence.source}')
            output_list.append(speech_response)

        return TTSResponse(audio=output_list, config=audio_config)
    except Exception as e:
        LOGGER.exception('Failed to infer %s', e)
        raise e


def infer_tts(language: str, gender: str, text_to_infer: str):
    choice = language + "_" + gender
    LOGGER.debug(f'choice for model {choice}')

    if choice in model_service.available_choice.keys():
        t2s = model_service.available_choice[choice]
    else:
        raise NotImplementedError('Requested model not found')

    if text_to_infer:
        text_to_infer = normalize_text(text_to_infer, language)

        # if len(text_to_infer) > settings.tts_max_text_limit:
        LOGGER.debug("Running in paragraph mode...")
        audio, sr = run_tts_paragraph(text_to_infer, language, t2s)
        torch.cuda.empty_cache()  # TODO: find better approach for this
        LOGGER.debug(f'Audio generated successfully with length {len(audio)}')
        low_sampled_audio = nnresample.resample(audio, SAMPLE_RATE, sr)
        low_sampled_audio = low_sampled_audio.astype('<' + low_sampled_audio.dtype.str[1:], copy=False)
        LOGGER.debug(f'Audio sampled successfully with length {len(low_sampled_audio)}')
        bytes_wav = bytes()
        byte_io = io.BytesIO(bytes_wav)
        write(byte_io, sr, low_sampled_audio)
        encoded_bytes = base64.b64encode(byte_io.read())
        encoded_string = encoded_bytes.decode()
        LOGGER.debug(f'Encoded Audio string {encoded_string}')
        return AudioFile(audioContent=encoded_string, samplingRate=SAMPLE_RATE)
    else:
        raise HTTPException(status_code=400, detail={"error": "No text"})


def split_sentences(paragraph, language):
    if language == "en":
        with MosesSentenceSplitter(language) as splitter:
            return splitter([paragraph])
    elif language in _INDIC:
        return sentence_tokenize.sentence_split(paragraph, lang=language)


def normalize_text(text, lang):
    if lang in _PURAM_VIRAM_LANGUAGES:
        text = text.replace('|', '।')
        text = text.replace('.', '।')
    return text


def pre_process_text(text, lang):
    if lang == 'hi':
        text = text.replace('।', '.')  # only for hindi models
    return text


def run_tts_paragraph(text, lang, t2s):
    audio_list = []
    split_sentences_list = split_sentences(text, language=lang)

    for sent in split_sentences_list:
        audio, sr = run_tts(pre_process_text(sent, lang), lang, t2s)
        audio_list.append(audio)

    concatenated_audio = np.concatenate([i for i in audio_list])
    # write(filename='temp_long.wav', rate=sr, data=concatenated_audio)
    return concatenated_audio, sr


def run_tts(text, lang, t2s):
    text_num_to_word = normalize_nums(text, lang)  # converting numbers to words in lang
    if lang != 'or':
        text_num_to_word_and_transliterated = model_service.transliterate_obj.translit_sentence(text_num_to_word,
                                                                                                lang)  # transliterating english words to lang
    else:
        text_num_to_word_and_transliterated = text_num_to_word
    mel = t2s[0].generate_mel(' ' + text_num_to_word_and_transliterated)
    audio, sr = t2s[1].generate_wav(mel)
    return audio, sr
