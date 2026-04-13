"""
Text improvement using Ollama LLM for SpeakType application.

This module handles sending transcribed text to Ollama for improvement,
including grammar correction, punctuation, and readability enhancement.
"""

import requests


class TextImprover:

    def __init__(self, config):
        self.config = config.config
        self.ollama_config = config.get_ollama_config()
        self.api_url = f"{self.ollama_config['host']}/api/generate"

    def improve_text(self, text):

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
        template = self.ollama_config.get("prompt_template")
        return template.replace("{text}", text)

    def _make_api_request(self, prompt):
        url = self.api_url
        payload = {
            "model": self.ollama_config.get("model"),
            "prompt": prompt,
            "max_token": 150,
            "stream": False,
        }

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"response={response.text}, status_code={response.status_code}")
                raise Exception("Failed to make API request to Ollama")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            raise Exception(f"Network error when calling Ollama API: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise Exception(f"Unexpected error when calling Ollama API: {e}")

    def _extract_improved_text(self, response_data):
        if response_data:
            response = response_data.get("response")
            return response.strip() if response else None
        return None
