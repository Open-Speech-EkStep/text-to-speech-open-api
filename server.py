import base64
import json
import os
from typing import Optional
import io
import numpy as np
import torch
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from indicnlp.tokenize import sentence_tokenize
from mosestokenizer import *
from pydantic import BaseModel
from tts_infer.num_to_word_on_sent import normalize_nums
from tts_infer.transliterate import XlitEngine
from tts_infer.tts import TextToMel, MelToWav
from scipy.io.wavfile import read, write

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TextJson(BaseModel):
    text: str
    lang: Optional[str] = "hi"
    gender: Optional[str] = "male"


max_text_limit = 450
INDIC = ["as", "bn", "gu", "hi", "kn", "ml", "mr", "or", "pa", "ta", "te"]
MODEL_BASE_PATH = os.environ.get('models_base_path', '')
gpu_present = torch.cuda.is_available()
print("Gpu present : ", gpu_present)
DEVICE = "cuda" if gpu_present else "cpu"
model_config_file_path = MODEL_BASE_PATH + 'model_dict.json'
if os.path.exists(model_config_file_path):
    with open(model_config_file_path, 'r') as f:
        model_config = json.load(f)
else:
    raise Exception(f'Model configuration file is missing at {model_config_file_path}')

supported_languages = list(model_config.keys())
available_choice = {}
for language_code, lang_config in model_config.items():
    available_choice[f"{language_code}_male"] = [
        TextToMel(glow_model_dir=MODEL_BASE_PATH + lang_config.get("male_glow"), device=DEVICE),
        MelToWav(hifi_model_dir=MODEL_BASE_PATH + lang_config.get("male_hifi"), device=DEVICE)]
    available_choice[f"{language_code}_female"] = [
        TextToMel(glow_model_dir=MODEL_BASE_PATH + lang_config.get("female_glow"), device=DEVICE),
        MelToWav(hifi_model_dir=MODEL_BASE_PATH + lang_config.get("female_hifi"), device=DEVICE)]

transliterate_obj = XlitEngine()

print(available_choice)


def split_sentences(paragraph, language):
    if language == "en":
        with MosesSentenceSplitter(language) as splitter:
            return splitter([paragraph])
    elif language in INDIC:
        return sentence_tokenize.sentence_split(paragraph, lang=language)


def pre_process_text(text, lang):
    if lang == 'hi':
        text = text.replace('।', '.')  # only for hindi models
    return text


def run_tts(text, lang, t2s):
    text_num_to_word = normalize_nums(text, lang)  # converting numbers to words in lang
    text_num_to_word_and_transliterated = transliterate_obj.translit_sentence(text_num_to_word,
                                                                              lang)  # transliterating english words to lang
    mel = t2s[0].generate_mel(' ' + text_num_to_word_and_transliterated)
    audio, sr = t2s[1].generate_wav(mel)
    return audio, sr


def run_tts_paragraph(text, lang, t2s):
    audio_list = []
    split_sentences_list = split_sentences(text, language='hi')

    for sent in split_sentences_list:
        audio, sr = run_tts(sent, lang, t2s)
        audio_list.append(audio)

    concatenated_audio = np.concatenate([i for i in audio_list])
    # write(filename='temp_long.wav', rate=sr, data=concatenated_audio)
    return concatenated_audio, sr


@app.post("/TTS/")
async def tts(input: TextJson):
    text = input.text
    lang = input.lang
    gender = input.gender

    choice = lang + "_" + gender
    if choice in available_choice.keys():
        t2s = available_choice[choice]
    else:
        raise HTTPException(
            status_code=400, detail={"error": "Requested model not found"}
        )

    if text:
        # text = pre_process_text(text, lang)
        if len(text) > max_text_limit:
            print("Running in paragraph mode...")
            audio, sr = run_tts_paragraph(text, lang, t2s)
        else:
            print("Running in text mode...")
            audio, sr = run_tts(text, lang, t2s)
        torch.cuda.empty_cache()
        print(audio)
        bytes_wav = bytes()
        byte_io = io.BytesIO(bytes_wav)
        write(byte_io, sr, audio)
        encoded_bytes = base64.b64encode(byte_io.read())
        encoded_string = encoded_bytes.decode()
        # write(filename='out.wav', rate=sr, data=audio) #If persisting of files are needed
    else:
        raise HTTPException(status_code=400, detail={"error": "No text"})

    ## to return outpur as a file
    # audio = open('out.wav', mode='rb')
    # return StreamingResponse(audio, media_type="audio/wav")

    # with open("out.wav", "rb") as audio_file:
    #     encoded_bytes = base64.b64encode(audio_file.read())
    #     encoded_string = encoded_bytes.decode()
    return {"encoding": "base64", "data": encoded_string, "sr": sr}


if __name__ == "__main__":
    uvicorn.run(
        "server:app", host="0.0.0.0", port=5000, log_level="info", reload=True
    )
