import unittest

from pydantic import ValidationError

from src.model.language import Language


class LanguageTest(unittest.TestCase):

    def testLanguage(self):
        language = Language(sourceLanguage='hi')
        self.assertEqual(language.sourceLanguage, 'hi', 'language does not match')

    def testLanguageRequiredValues(self):
        try:
            config = Language()
            self.fail('Expected validation error got nothing')
        except ValidationError as e:
            pass
        except Exception as er:
            self.fail(f'Expected validation error for {er}')


if __name__ == '__main__':
    unittest.main()
