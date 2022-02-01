import unittest

from pydantic import ValidationError

from src.model.tts_request import TTSRequest, Sentence, TTSConfig, Language


class TTSRequestTest(unittest.TestCase):

    def test_request(self):
        request = TTSRequest(input=[Sentence(source='ABC')],
                             config=TTSConfig(gender='female', language=Language(sourceLanguage='en')))
        self.assertEqual(request.input[0].source, 'ABC', 'Text does not match')
        self.assertEqual(request.config.language.sourceLanguage, 'en', 'Language does not match')
        self.assertEqual(request.config.gender, 'female', 'Gender does not match')

    def test_required_values(self):
        try:
            request = TTSRequest()
            self.fail('Expected validation error got nothing')
        except ValidationError as e:
            pass
        except Exception as er:
            self.fail(f'Expected validation error for {er}')

    def test_config_is_required(self):
        try:
            request = TTSRequest(input=[Sentence(source='ABC')])
            self.fail('Expected validation error got nothing')
        except ValidationError as e:
            pass
        except Exception as er:
            self.fail(f'Expected validation error for {er}')

    def test_input_is_required(self):
        try:
            request = TTSRequest(input=[Sentence(source='ABC')])
            self.fail('Expected validation error got nothing')
        except ValidationError as e:
            pass
        except Exception as er:
            self.fail(f'Expected validation error for {er}')

    def test_TTSConfig_without_gender(self):
        try:
            config = TTSConfig(language=Language(sourceLanguage='en'))
        except ValidationError as e:
            self.assertEqual(e.errors()[0]['type'], 'value_error.missing')
            self.assertEqual(e.errors()[0]['loc'][0], 'gender')
            pass
        except Exception as er:
            self.fail(f'Expected validation error for {er}')

    def test_TTSConfig_empty_gender(self):
        try:
            config = TTSConfig(language=Language(sourceLanguage='en'), gender='')
        except ValidationError as e:
            self.assertEqual(e.errors()[0]['loc'][0], 'gender')
            self.assertEqual(e.errors()[0]['msg'], 'gender cannot be empty')
            pass
        except Exception as er:
            self.fail(f'Expected validation error for {er}')

    def test_TTSConfig_empty_sourceLanguage(self):
        try:
            config = TTSConfig(language=Language(sourceLanguage=''), gender='male')
        except ValidationError as e:
            self.assertEqual(e.errors()[0]['loc'][0], 'sourceLanguage')
            self.assertEqual(e.errors()[0]['msg'], 'sourceLanguage cannot be empty')
            pass
        except Exception as er:
            self.fail(f'Expected validation error for {er}')

    def test_TTSConfig(self):
        try:
            config = TTSConfig(gender='male')
        except ValidationError as e:
            self.assertEqual(len(e.errors()), 1)
            self.assertEqual(e.errors()[0]['type'], 'value_error.missing')
            self.assertEqual(e.errors()[0]['loc'][0], 'language')
            pass
        except Exception as er:
            self.fail(f'Expected validation error for {er}')

    def test_TTSConfig_unsupported_gender(self):

        try:
            config = TTSConfig(language=Language(sourceLanguage='en'), gender='Male')
        except ValidationError as e:
            self.assertEqual(len(e.errors()), 1)
            self.assertEqual(e.errors()[0]['type'], 'value_error')
            self.assertEqual(e.errors()[0]['loc'][0], 'gender')
            self.assertEqual(e.errors()[0]['msg'], 'Unsupported gender value')
            pass
        except Exception as er:
            self.fail(f'Expected validation error for {er}')

    def test_sentence_empty_source(self):
        try:
            sentence = Sentence(source='')
        except ValidationError as e:
            self.assertEqual(len(e.errors()), 1)
            self.assertEqual(e.errors()[0]['type'], 'value_error')
            self.assertEqual(e.errors()[0]['loc'][0], 'source')
            self.assertEqual(e.errors()[0]['msg'], 'source cannot be empty')
            pass
        except Exception as er:
            self.fail(f'Expected validation error for {er}')

    def test_sentence(self):
        sentence = Sentence(source='Text')
        self.assertEqual(sentence.source, 'Text')

    def test_empty_input(self):
        try:
            request = TTSRequest(input=[], config=TTSConfig(gender='female', language=Language(sourceLanguage='en')))
        except ValidationError as e:
            self.assertEqual(len(e.errors()), 1)
            self.assertEqual(e.errors()[0]['type'], 'value_error')
            self.assertEqual(e.errors()[0]['loc'][0], 'input')
            self.assertEqual(e.errors()[0]['msg'], 'input cannot be empty')
            pass
        except Exception as er:
            self.fail(f'Expected validation error for {er}')


if __name__ == '__main__':
    unittest.main()
