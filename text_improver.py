"""
Text improvement using Ollama LLM for SpeakType application.

This module handles sending transcribed text to Ollama for improvement,
including grammar correction, punctuation, and readability enhancement.

LEARNING NOTE: This file demonstrates:
- Making HTTP requests to local APIs
- Building prompts for LLMs
- Processing text responses
- Error handling for network requests
"""

import requests


class TextImprover:
    """
    Handles text improvement using Ollama LLM.

    LEARNING NOTE: This class shows how to:
    - Build effective prompts for text improvement
    - Make API calls to local services
    - Handle different response formats
    - Provide fallback behavior
    """

    def __init__(self, config):
        """
        Initialize the text improver with configuration.

        Args:
            config: Configuration object with ollama settings

        TODO: Implement this method to:
        1. Store config as instance variable
        2. Extract ollama settings (host, model, prompt template)
        3. Validate that required settings are present
        4. Set up API endpoint URL
        """

        self.config = config.config
        self.ollama_config = config.get_ollama_config()
        self.api_url = f"{self.ollama_config['host']}/api/generate"

    def improve_text(self, text):
        """
        Improve the given text using Ollama LLM.

        Args:
            text: Original transcribed text to improve

        Returns:
            Improved text, or original text if improvement fails

        LEARNING NOTE: This method demonstrates:
        - Building structured prompts for LLMs
        - Making POST requests with JSON payloads
        - Processing streaming or complete responses
        - Graceful error handling with fallbacks

        TODO: Implement this method to:
        1. Check if text is empty or too short (return as-is)
        2. Build prompt using the template from config
        3. Create API request payload with:
           - model: The LLM model to use
           - prompt: The formatted prompt with original text
           - stream: False (for complete response)
           - options: Additional model parameters
        4. Make POST request to Ollama API endpoint
        5. Extract improved text from response
        6. Return improved text, or original if API fails
        7. Add timeout and retry logic for robustness
        """

        if len(text) <= 10:
            return text

        prompt = self._build_prompt(text)
        response_data = self._make_api_request(prompt)

        if response_data is None:
            raise Exception("No response from Ollama")

        improved_text = self._extract_improved_text(response_data)
        if improved_text is None:
            raise Exception("No improved text extracted from response")

        return improved_text

    def _build_prompt(self, text):
        """
        Build a prompt for the LLM using the template from config.
        """

        template = self.ollama_config.get("prompt_template")
        return template.replace("{text}", text)

    def _make_api_request(self, prompt):
        """
        Make API request to Ollama with the given prompt.
        """
        url = self.api_url
        payload = {
            "model": self.ollama_config.get("model"),
            "prompt": prompt,
            "max_token": 150,
            "stream": False,
        }

        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"response={response.text}, status_code={response.status_code}")
            raise Exception("Failed to make API request to Ollama")

    def _extract_improved_text(self, response_data):
        """
        Extract the improved text from API response.
        """
        if response_data:
            response = response_data.get("response")
            return response.strip() if response else None
        return None
