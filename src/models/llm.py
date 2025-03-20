#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
LLM Interface

Provides a standardized interface for interacting with large language models.
"""

import os
import logging
from typing import Any, Dict, List, Optional, Union

from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

# Setup logging
logger = logging.getLogger(__name__)

class LLMInterface:
    """
    Interface for Large Language Models
    
    Provides a standardized way to interact with different LLMs,
    with OpenAI's GPT models as the default implementation.
    """
    
    def __init__(
        self,
        client: Optional[Any] = None,
        model_name: str = "gpt-4",
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ):
        """
        Initialize the LLM interface.
        
        Args:
            client: Optional pre-configured OpenAI client
            model_name: Name of the model to use
            temperature: Temperature parameter for generation
            max_tokens: Maximum tokens to generate
        """
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        # Initialize OpenAI client if not provided
        if client is None:
            self.client = openai.OpenAI(
                api_key=os.getenv("OPENAI_API_KEY")
            )
        else:
            self.client = client
        
        logger.info(f"LLMInterface initialized with model: {model_name}")
    
    def generate(self, prompt: str) -> str:
        """
        Generate text based on the prompt.
        
        Args:
            prompt: Input prompt for the model
            
        Returns:
            Generated text response
        """
        try:
            logger.debug(f"Generating response for prompt: {prompt[:50]}...")
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            result = response.choices[0].message.content
            logger.debug(f"Generated response: {result[:50]}...")
            return result
        
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return f"Error: {str(e)}"
    
    def generate_with_system(self, system_prompt: str, user_prompt: str) -> str:
        """
        Generate text with a system prompt and user prompt.
        
        Args:
            system_prompt: System instructions
            user_prompt: User query or input
            
        Returns:
            Generated text response
        """
        try:
            logger.debug(f"Generating response with system prompt")
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            result = response.choices[0].message.content
            logger.debug(f"Generated response: {result[:50]}...")
            return result
        
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return f"Error: {str(e)}"
    
    def generate_chat(self, messages: List[Dict[str, str]]) -> str:
        """
        Generate text based on a conversation history.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            
        Returns:
            Generated text response
        """
        try:
            logger.debug(f"Generating response for chat with {len(messages)} messages")
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            result = response.choices[0].message.content
            logger.debug(f"Generated response: {result[:50]}...")
            return result
        
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return f"Error: {str(e)}"
