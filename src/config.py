from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "TTS API"
    server_port: int = 5000
    log_level: str = 'INFO'
    gpu: bool = False
    max_worker: int = 50
    tts_max_text_limit: int = 450
    models_base_path: str = ''
    model_config_file_path: str = models_base_path + 'model_dict.json'


settings = Settings()
