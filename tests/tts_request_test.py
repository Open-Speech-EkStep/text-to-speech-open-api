import unittest

from pydantic import ValidationError

from src.model.tts_request import TTSRequest, Sentence, TTSConfig, Language


class TTSRequestTest(unittest.TestCase):

    def testRequest(self):
        request = TTSRequest(input=[Sentence(source='ABC')],
                             config=TTSConfig(gender='female', language=Language(sourceLanguage='en')))
        self.assertEqual(request.input[0].source, 'ABC', 'Text does not match')
        self.assertEqual(request.config.language.sourceLanguage, 'en', 'Language does not match')
        self.assertEqual(request.config.gender, 'female', 'Gender does not match')

    def testTextIsRequiredValues(self):
        try:
            request = TTSRequest()
            self.fail('Expected validation error got nothing')
        except ValidationError as e:
            pass
        except Exception as er:
            self.fail(f'Expected validation error for {er}')

    def testConfigIsRequired(self):
        try:
            request = TTSRequest(input=[Sentence(source='ABC')])
            self.fail('Expected validation error got nothing')
        except ValidationError as e:
            pass
        except Exception as er:
            self.fail(f'Expected validation error for {er}')

    def testInoutIsRequired(self):
        try:
            request = TTSRequest(input=[Sentence(source='ABC')])
            self.fail('Expected validation error got nothing')
        except ValidationError as e:
            pass
        except Exception as er:
            self.fail(f'Expected validation error for {er}')


if __name__ == '__main__':
    unittest.main()
