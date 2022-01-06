import base64
import json
import os
from typing import Optional

import torch
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from scipy.io.wavfile import write
from tts_infer.num_to_word_on_sent import normalize_nums
from tts_infer.transliterate import XlitEngine
from tts_infer.tts import TextToMel, MelToWav

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
# glow_hi_male = TextToMel(glow_model_dir="", device="")
# glow_hi_female = TextToMel(glow_model_dir="", device="")
# hifi_hi = MelToWav(hifi_model_dir="", device="")

# available_choice = {
#     "hi_male": [glow_hi_male, hifi_hi],
#     "hi_female": [glow_hi_female, hifi_hi],
# }

print(available_choice)


def pre_process_text(text, lang):
    if lang == 'hi':
        text = text.replace('।', '.')  # only for hindi models
    return text


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
        text = pre_process_text(text, lang)
        text_num_to_word = normalize_nums(text, lang)  # converting numbers to words in lang
        text_num_to_word_and_transliterated = transliterate_obj.translit_sentence(text_num_to_word,
                                                                                  lang)  # transliterating english words to lang
        mel = t2s[0].generate_mel(' ' + text_num_to_word_and_transliterated)
        data, sr = t2s[1].generate_wav(mel)
        write(filename='out.wav', rate=sr, data=data)
    else:
        raise HTTPException(status_code=400, detail={"error": "No text"})

    ## to return outpur as a file
    # audio = open('out.wav', mode='rb')
    # return StreamingResponse(audio, media_type="audio/wav")

    with open("out.wav", "rb") as audio_file:
        encoded_bytes = base64.b64encode(audio_file.read())
        encoded_string = encoded_bytes.decode()
    return {"encoding": "base64", "data": encoded_string, "sr": sr}


if __name__ == "__main__":
    uvicorn.run(
        "server:app", host="0.0.0.0", port=5000, log_level="info", reload=True
    )
