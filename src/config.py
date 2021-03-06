from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "TTS API"
    server_port: int = 5000
    log_level: str = 'DEBUG'
    gpu: bool = True
    tts_max_text_limit: int = 450
    models_base_path: str = ''
    model_config_file_path: str = 'model_dict.json'


settings = Settings()
