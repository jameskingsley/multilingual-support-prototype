import unittest
from unittest.mock import patch
from src.translator import translate_message

class TestTranslator(unittest.TestCase):
    
    @patch('src.translator.model')
    @patch('src.translator.tokenizer')
    def test_translate_message_mock(self, mock_tokenizer, mock_model):
        """Test translation pipeline with mocked model and tokenizer."""
        mock_tokenizer.lang_code_to_id = {"spa_Latn": 1, "eng_Latn": 2}
        mock_tokenizer.return_value = {"input_ids": [101, 102]}
        mock_model.generate.return_value = [[201, 202]]
        mock_tokenizer.decode.return_value = "Hello world"
        
        result = translate_message("Hola mundo", source_lang="spa_Latn", target_lang="eng_Latn")
        self.assertEqual(result, "Hello world")

if __name__ == '__main__':
    unittest.main()