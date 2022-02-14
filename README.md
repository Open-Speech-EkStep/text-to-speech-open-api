# Text to Speech API

### Documentation
**Project Documentation:**  https://open-speech-ekstep.github.io/tts_model_api/

**Api Documentation:** Swagger API document is hosted on `/docs` endpoint.

**Sample Request:**
```json
{
    "input": [
        {
            "source": "भारत मेरा देश है|"
        }
    ],
    "config": {
        "gender": "female",
        "language": {
            "sourceLanguage": "hi"
        }
    }
}
```

**Sample Response:**
```json
{
    "audio": [
        {
            "audioContent": "<Audio Bytes>"
        }
    ],
    "config": {
        "language": {
            "sourceLanguage": "hi"
        },
        "audioFormat": "wav",
        "encoding": "base64",
        "samplingRate": 22050
    }
}
```

### Supported environment variables

| **Variable Name**      | **Default Value** | **Description**                                                                                                   |
|------------------------|-------------------|-------------------------------------------------------------------------------------------------------------------|
| server_port            | 5000              | Port for unicorn server                                                                                           |
| log_level              | DEBUG             | Log level for application logs                                                                                    |
| gpu                    | True              | True: Load the models on GPU False: Use CPU                                                                       |
| tts_max_text_limit     | 450               | Maximum length of text that will be sent to model. Text above this will be broken in chunks before hitting model. |
| models_base_path       |                   | Location for language model folders.                                                                              |
| model_config_file_path | model_dict.json   |                                                                                                                   |

### Running with Docker image

