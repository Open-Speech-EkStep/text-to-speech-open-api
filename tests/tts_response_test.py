import unittest

from pydantic import ValidationError

from src.model.tts_response import TTSResponse


class TTSResponseTest(unittest.TestCase):

    def testRequest(self):
        response = TTSResponse(data='data', sr='sample rate')
        self.assertEqual(response.data, 'data', 'data does not match')
        self.assertEqual(response.sr, 'sample rate', 'sample rate does not match')
        self.assertEqual(response.encoding, 'base64', 'default value for encoding is not set')

    def testTextIsRequired(self):
        try:
            response = TTSResponse()
            self.fail('Expected validation error got nothing')
        except ValidationError as e:
            pass
        except Exception as er:
            self.fail(f'Expected validation error for {er}')


if __name__ == '__main__':
    unittest.main()
