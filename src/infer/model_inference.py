import json
import os

import torch
from mosestokenizer import *
from tts_infer.transliterate import XlitEngine
from tts_infer.tts import TextToMel, MelToWav

from src import log_setup, utilities
from src.config import settings

LOGGER = log_setup.get_logger(__name__)


class ModelService:

    def __init__(self):
        gpu_present = torch.cuda.is_available()
        LOGGER.info("Gpu present : %s", gpu_present)
        LOGGER.info(f'Loading with settings {settings}')

        self.device = "cuda" if gpu_present & settings.gpu else "cpu"
        LOGGER.info("Using device : %s", self.device)

        model_config_file_path = settings.models_base_path+settings.model_config_file_path
        if os.path.exists(model_config_file_path):
            with open(model_config_file_path, 'r') as f:
                model_config = json.load(f)
        else:
            raise Exception(f'Model configuration file is missing at {model_config_file_path}')
        languages = list(utilities.get_env_var('languages', ['all']))
        self.supported_languages = list(model_config.keys())
        LOGGER.info(f'supported languages {self.supported_languages}')
        self.available_choice = {}
        for language_code, lang_config in model_config.items():
            if language_code in languages or 'all' in languages:
                self.available_choice[f"{language_code}_male"] = [
                    TextToMel(glow_model_dir=settings.models_base_path + lang_config.get("male_glow"),
                              device=self.device),
                    MelToWav(hifi_model_dir=settings.models_base_path + lang_config.get("male_hifi"),
                             device=self.device)]
                self.available_choice[f"{language_code}_female"] = [
                    TextToMel(glow_model_dir=settings.models_base_path + lang_config.get("female_glow"),
                              device=self.device),
                    MelToWav(hifi_model_dir=settings.models_base_path + lang_config.get("female_hifi"),
                             device=self.device)]
                LOGGER.info(f'{language_code} Models initialized successfully')
            LOGGER.info(f'Model service available_choices are {self.available_choice}')
        self.transliterate_obj = XlitEngine()
