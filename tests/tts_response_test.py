import unittest

from pydantic import ValidationError

from src.model.language import Language
from src.model.tts_response import TTSResponse, AudioConfig, AudioFile


class TTSResponseTest(unittest.TestCase):

    def testRequest(self):
        response = TTSResponse(audio=[AudioFile(audioContent='data')],
                               config=AudioConfig(language=Language(sourceLanguage='hi')))
        self.assertEqual(response.audio[0].audioContent, 'data', 'content does not match')
        self.assertEqual(response.config.language.sourceLanguage, 'hi', 'language does not match')
        self.assertEqual(response.config.samplingRate, 22050, 'default value for sample rate does not match')
        self.assertEqual(response.config.encoding, 'base64', 'default value for encoding is not set')
        self.assertEqual(response.config.audioFormat, 'wav', 'default value for audio format is not set')

    def testTextIsRequiredValues(self):
        try:
            response = TTSResponse()
            self.fail('Expected validation error got nothing')
        except ValidationError as e:
            pass
        except Exception as er:
            self.fail(f'Expected validation error for {er}')

    def testResponseRequiredConfig(self):
        try:
            response = TTSResponse(audio=[AudioFile(audioContent='data')])
            self.fail('Expected validation error got nothing')
        except ValidationError as e:
            pass
        except Exception as er:
            self.fail(f'Expected validation error for {er}')

    def testResponseRequiredAudio(self):
        try:
            response = TTSResponse(config=AudioConfig(language='hi'))
            self.fail('Expected validation error got nothing')
        except ValidationError as e:
            pass
        except Exception as er:
            self.fail(f'Expected validation error for {er}')

    def testAudioConfigRequiredValues(self):
        try:
            config = AudioConfig()
            self.fail('Expected validation error got nothing')
        except ValidationError as e:
            pass
        except Exception as er:
            self.fail(f'Expected validation error for {er}')

    def testAudioConfigWithFiles(self):
        config = AudioConfig(language=Language(sourceLanguage='hi'))
        self.assertEqual(config.language.sourceLanguage, 'hi', 'language does not match')


if __name__ == '__main__':
    unittest.main()
