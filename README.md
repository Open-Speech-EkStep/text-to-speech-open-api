# Text to Speech API


Swagger API document is hosted on `/docs` endpoint.

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