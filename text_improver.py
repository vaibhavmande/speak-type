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

# TODO: Import requests for HTTP API calls
# Install with: pip install requests
# import requests

# TODO: Import json for API request/response handling
# import json

# TODO: Import time for timeout handling
# import time


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
        pass
    
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
        pass
    
    def _build_prompt(self, text):
        """
        Build a prompt for the LLM using the template from config.
        
        Args:
            text: Original text to include in prompt
            
        Returns:
            Formatted prompt string
            
        LEARNING NOTE: This method demonstrates:
        - String formatting and templating
        - Configuration-driven prompt engineering
        - Text preprocessing
        
        TODO: Implement this method to:
        1. Get prompt template from config
        2. Replace {text} placeholder with actual text
        3. Clean up any formatting issues
        4. Return the formatted prompt
        """
        pass
    
    def _make_api_request(self, prompt):
        """
        Make API request to Ollama with the given prompt.
        
        Args:
            prompt: Formatted prompt to send to LLM
            
        Returns:
            API response data, or None if request fails
            
        LEARNING NOTE: This method demonstrates:
        - HTTP POST requests with JSON
        - API error handling
        - Response validation
        - Network timeout management
        
        TODO: Implement this method to:
        1. Set up request headers (Content-Type: application/json)
        2. Create request payload with model and prompt
        3. Make POST request to Ollama generate endpoint
        4. Handle different response status codes
        5. Parse JSON response
        6. Return response data or None on failure
        7. Implement retry logic for transient errors
        """
        pass
    
    def _extract_improved_text(self, response_data):
        """
        Extract the improved text from API response.
        
        Args:
            response_data: Raw API response data
            
        Returns:
            Improved text string, or None if extraction fails
            
        LEARNING NOTE: This method demonstrates:
        - JSON data extraction
        - Response validation
        - Data cleaning and formatting
        
        TODO: Implement this method to:
        1. Check if response contains expected fields
        2. Extract the generated text from response
        3. Clean up any extra whitespace or formatting
        4. Validate that improved text is not empty
        5. Return the cleaned text or None
        """
        pass
    
    def test_connection(self):
        """
        Test connection to Ollama API.
        
        Returns:
            True if connection successful, False otherwise
            
        LEARNING NOTE: This method demonstrates:
        - Health checking for external services
        - Simple API connectivity tests
        - Service availability validation
        
        TODO: Implement this method to:
        1. Make simple request to Ollama API
        2. Check if service responds
        3. Return True if healthy, False otherwise
        """
        pass
    
    def get_available_models(self):
        """
        Get list of available models from Ollama.
        
        Returns:
            List of model names, or empty list if request fails
            
        LEARNING NOTE: This method demonstrates:
        - Discovering available resources from APIs
        - Dynamic configuration options
        - API endpoint exploration
        
        TODO: Implement this method to:
        1. Make request to Ollama models endpoint
        2. Parse list of available models
        3. Return model names as list
        4. Return empty list if request fails
        """
        pass
    
    def is_available(self):
        """
        Check if Ollama service is available.
        
        Returns:
            True if service is available, False otherwise
            
        TODO: Implement this method to:
        1. Use test_connection() to check service
        2. Cache result for short period to avoid repeated checks
        3. Return availability status
        """
        pass
