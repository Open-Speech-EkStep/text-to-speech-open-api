import unittest

from pydantic import ValidationError

from src.model.tts_request import TTSRequest


class TTSRequestTest(unittest.TestCase):

    def testRequest(self):
        request = TTSRequest(text='ABC', lang='en', gender='female')
        self.assertEqual(request.text, 'ABC', 'Text does not match')
        self.assertEqual(request.lang, 'en', 'Language does not match')
        self.assertEqual(request.gender, 'female', 'Gender does not match')

    def testTextIsRequired(self):
        try:
            request = TTSRequest(lang='en', gender='female')
            self.fail('Expected validation error got nothing')
        except ValidationError as e:
            pass
        except Exception as er:
            self.fail(f'Expected validation error for {er}')


if __name__ == '__main__':
    unittest.main()
