import unittest

from src.config import Settings


class ConfigTest(unittest.TestCase):

    def testDefaultValues(self):
        settings = Settings()
        self.assertEqual(settings.app_name, 'TTS API', 'app_name default value does not match')
        self.assertEqual(settings.server_port, 5000, 'server_port default value does not match')
        self.assertEqual(settings.gpu, True, 'gpu default value does not match')
        self.assertEqual(settings.tts_max_text_limit, 450, 'tts_max_text_limit default value does not match')
        self.assertEqual(settings.models_base_path, '', 'models_base_path default value does not match')
        self.assertEqual(settings.model_config_file_path, 'model_dict.json',
                         'model_dict.json default value does not match')


if __name__ == '__main__':
    unittest.main()
