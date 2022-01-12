import json
import os

import torch
from mosestokenizer import *
from tts_infer.tts import TextToMel, MelToWav
from tts_infer.num_to_word_on_sent import normalize_nums
from tts_infer.transliterate import XlitEngine

from src.config import settings


class ModelService:

    def __init__(self):
        gpu_present = torch.cuda.is_available()
        print("Gpu present : ", gpu_present)
        self.device = "cuda" if gpu_present else "cpu"
        model_config_file_path = settings.model_config_file_path
        if os.path.exists(model_config_file_path):
            with open(model_config_file_path, 'r') as f:
                model_config = json.load(f)
        else:
            raise Exception(f'Model configuration file is missing at {model_config_file_path}')

        self.supported_languages = list(model_config.keys())
        self.available_choice = {}
        for language_code, lang_config in model_config.items():
            self.available_choice[f"{language_code}_male"] = [
                TextToMel(glow_model_dir=settings.models_base_path + lang_config.get("male_glow"), device=self.device),
                MelToWav(hifi_model_dir=settings.models_base_path + lang_config.get("male_hifi"), device=self.device)]
            self.available_choice[f"{language_code}_female"] = [
                TextToMel(glow_model_dir=settings.models_base_path + lang_config.get("female_glow"),
                          device=self.device),
                MelToWav(hifi_model_dir=settings.models_base_path + lang_config.get("female_hifi"), device=self.device)]

            print(self.available_choice)
            self.transliterate_obj = XlitEngine()
