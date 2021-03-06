# Text to Speech API

### Documentation for TTS
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

You can use a pre-built image of this repo to run in docker. Models are open sourced in our https://github.com/Open-Speech-EkStep/vakyansh-models.

Pre-built docker images are hosted on `gcr.io/ekstepspeechrecognition/speech_recognition_model_api`.
We do not follow the latest tag, so you have to use a specific tag.

```
docker pull gcr.io/ekstepspeechrecognition/text_to_speech_open_api:2.1.15
```

**Running with docker**

```shell
docker run -itd -p 5000:5000 --gpus all -v <your location for deployed_models>:/opt/text_to_speech_open_api/deployed_models/ -v <your location for translit_models>:/opt/text_to_speech_open_api/vakyansh-tts/src/glow_tts/tts_infer/translit_models/ gcr.io/ekstepspeechrecognition/text_to_speech_open_api:2.1.15
```


**Directory structure of `/opt/text_to_speech_open_api/deployed_models/`**

```shell
.
|-- gujarati
|   |-- female
|   |   |-- glow_tts
|   |   |   |-- G_190.pth
|   |   |   `-- config.json
|   |   `-- hifi_tts
|   |       |-- config.json
|   |       `-- g_00100000
|   `-- male
|       |-- glow_tts
|       |   |-- G_170.pth
|       |   `-- config.json
|       `-- hifi_tts
|           |-- config.json
|           `-- g_00100000
|-- hindi
|   |-- female
|   |   |-- glow_tts
|   |   |   |-- G_100.pth
|   |   |   |-- G_250.pth
|   |   |   `-- config.json
|   |   `-- hifi_tts
|   |       |-- config.json
|   |       `-- g_00100000
|   `-- male
|       |-- glow_tts
|       |   |-- G_100.pth
|       |   `-- config.json
|       `-- hifi_tts
|           |-- config.json
|           `-- g_00200000
```

**Directory structure for `/opt/text_to_speech_open_api/vakyansh-tts/src/glow_tts/tts_infer/translit_models/`** translit models will be downloaded automatically.

```shell
.
|-- README.md
|-- bengali
|   |-- bn_101_model.pth
|   |-- bn_scripts.json
|   `-- bn_words_a4b.json
|-- default_lineup.json
|-- gujarati
|   |-- gu_101_model.pth
|   |-- gu_scripts.json
|   `-- gu_words_a4b.json
|-- hindi
|   |-- hi_111_model.pth
|   |-- hi_scripts.json
|   |-- hi_words_a4b.json
```

**Sample model_dict.json**

```yaml
{
  "hi": {
    "male_glow": "hindi/male/glow_tts",
    "male_hifi": "hindi/male/hifi_tts",
    "female_glow": "hindi/female/glow_tts",
    "female_hifi": "hindi/female/hifi_tts"
  },
  "ta": {
    "male_glow": "tamil/male/glow_tts",
    "male_hifi": "tamil/male/hifi_tts",
    "female_glow": "tamil/female/glow_tts",
    "female_hifi": "tamil/female/hifi_tts"
  }
}
```

### Building from source

We build this app in two steps to expedite the process of changes in the main source. We build a dependency image `gcr.io/ekstepspeechrecognition/text_to_speech_open_api_dependency
` for which you can find dependency docker image file at [dependencies/Dockerfile](dependencies/Dockerfile). 
Using dependency image, we build the main images which are published at `gcr.io/ekstepspeechrecognition/text_to_speech_open_api`. Docker file for this step is available [here](Dockerfile).
You can use these steps to recreate the bundle. We recommend using some environment manager like [conda](https://github.com/conda/conda).