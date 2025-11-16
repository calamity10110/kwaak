
import unittest
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock
from orchestrator.llm.openai import OpenAIProvider

class TestOpenAIProvider(unittest.TestCase):
    @patch('orchestrator.llm.openai.AsyncOpenAI')
    def test_generate(self, mock_openai_class):
        # Arrange
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        mock_choice = MagicMock()
        mock_choice.message.content = "Test response"

        mock_response = MagicMock()
        mock_response.choices = [mock_choice]

        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        provider = OpenAIProvider(api_key="test_key")

        # Act
        response = asyncio.run(provider.generate("Test prompt"))

        # Assert
        self.assertEqual(response, "Test response")

    @patch('orchestrator.llm.openai.AsyncOpenAI')
    def test_embed(self, mock_openai_class):
        # Arrange
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        mock_embedding = MagicMock()
        mock_embedding.embedding = [0.1, 0.2, 0.3]

        mock_response = MagicMock()
        mock_response.data = [mock_embedding]

        mock_client.embeddings.create = AsyncMock(return_value=mock_response)

        provider = OpenAIProvider(api_key="test_key")

        # Act
        embedding = asyncio.run(provider.embed("Test text"))

        # Assert
        self.assertEqual(embedding, [0.1, 0.2, 0.3])

if __name__ == '__main__':
    unittest.main()
