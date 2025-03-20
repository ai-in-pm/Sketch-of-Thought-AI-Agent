#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Sketch-of-Thought Reasoner

Implements the Sketch-of-Thought reasoning paradigms for efficient cognitive processing.
"""

import logging
from typing import Any, Dict, List, Optional, Tuple, Union

from models.llm import LLMInterface

# Setup logging
logger = logging.getLogger(__name__)

class SoTReasoner:
    """
    Sketch-of-Thought Reasoner
    
    This class implements the SoT reasoning paradigms:
    - Conceptual Chaining: linking key concepts with minimal words
    - Chunked Symbolism: compressing quantitative reasoning into grouped symbols
    - Expert Lexicons: using domain-specific shorthand
    """
    
    def __init__(self, llm: LLMInterface):
        """
        Initialize the SoT Reasoner.
        
        Args:
            llm: The LLM interface for reasoning
        """
        self.llm = llm
        self.paradigms = {
            "conceptual_chaining": self._conceptual_chain_reason,
            "chunked_symbolism": self._chunked_symbolic_reason,
            "expert_lexicon": self._expert_lexicon_reason,
            "default": self._default_reason
        }
        logger.info("SoTReasoner initialized")
    
    def _select_paradigm(self, task: str, world_model: Dict[str, Any]) -> str:
        """
        Select the appropriate reasoning paradigm based on the task and context.
        
        Args:
            task: The reasoning task/query
            world_model: Current state of the world
            
        Returns:
            Selected reasoning paradigm name
        """
        # Implement paradigm selection logic here
        # This could be rule-based or ML-based
        
        # Check for mathematical/quantitative content
        math_indicators = [
            "calculate", "compute", "solve", "equation", "formula",
            "how many", "what is the value", "percent", "average",
            "+", "-", "*", "/", "=", ">", "<", "≤", "≥"
        ]
        
        # Check for domain-specific content
        domain_indicators = {
            "medical": ["patient", "diagnosis", "treatment", "symptom", "disease"],
            "programming": ["code", "function", "class", "algorithm", "variable"],
            "finance": ["stock", "investment", "portfolio", "return", "market"]
        }
        
        # Check for relational/conceptual content
        conceptual_indicators = [
            "relate", "connect", "compare", "contrast", "difference",
            "similarity", "causation", "impact", "effect", "influence",
            "why", "how does", "what causes", "relationship"
        ]
        
        # Default to conceptual chaining
        selected_paradigm = "conceptual_chaining"
        
        # Check for math indicators
        if any(indicator in task.lower() for indicator in math_indicators):
            selected_paradigm = "chunked_symbolism"
            logger.debug(f"Selected paradigm 'chunked_symbolism' based on task: {task[:50]}...")
            return selected_paradigm
        
        # Check for domain-specific indicators
        for domain, indicators in domain_indicators.items():
            if any(indicator in task.lower() for indicator in indicators):
                selected_paradigm = "expert_lexicon"
                logger.debug(f"Selected paradigm 'expert_lexicon' for domain '{domain}' based on task: {task[:50]}...")
                return selected_paradigm
        
        # Check for conceptual indicators
        if any(indicator in task.lower() for indicator in conceptual_indicators):
            selected_paradigm = "conceptual_chaining"
            logger.debug(f"Selected paradigm 'conceptual_chaining' based on task: {task[:50]}...")
            return selected_paradigm
        
        logger.debug(f"Using default paradigm '{selected_paradigm}' for task: {task[:50]}...")
        return selected_paradigm
    
    def _conceptual_chain_reason(self, task: str, world_model: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform reasoning using the Conceptual Chaining paradigm.
        
        This paradigm links key concepts or entities with minimal words,
        often using arrows or symbols.
        
        Args:
            task: The reasoning task/query
            world_model: Current state of the world
            
        Returns:
            Reasoning result in Conceptual Chaining format
        """
        # Create prompt for conceptual chaining
        prompt = f"""
        You are an AI reasoning using the Sketch-of-Thought (SoT) Conceptual Chaining paradigm.
        
        In Conceptual Chaining, you link key concepts with minimal words, using -> arrows.
        For example: Seoul -> South Korea -> Won (Currency)
        
        Current world state:
        {self._format_world_model(world_model)}
        
        Task: {task}
        
        Think step by step, but use concise concept chains. Respond in this format:
        
        <thinking>
        [Your condensed chain of concepts, using -> arrows]
        </thinking>
        
        <answer>
        [Your final answer/explanation based on the conceptual chain]
        </answer>
        """
        
        # Get response from LLM
        response = self.llm.generate(prompt)
        
        # Extract the thinking and answer parts
        thinking = self._extract_between(response, "<thinking>", "</thinking>")
        answer = self._extract_between(response, "<answer>", "</answer>")
        
        return {
            "paradigm": "conceptual_chaining",
            "thinking": thinking.strip(),
            "answer": answer.strip(),
            "full_response": response
        }
    
    def _chunked_symbolic_reason(self, task: str, world_model: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform reasoning using the Chunked Symbolism paradigm.
        
        This paradigm compresses quantitative reasoning into grouped symbols,
        such as equations or mathematical notations.
        
        Args:
            task: The reasoning task/query
            world_model: Current state of the world
            
        Returns:
            Reasoning result in Chunked Symbolism format
        """
        # Create prompt for chunked symbolism
        prompt = f"""
        You are an AI reasoning using the Sketch-of-Thought (SoT) Chunked Symbolism paradigm.
        
        In Chunked Symbolism, you compress quantitative reasoning into symbols and equations.
        For example: v_f = v_i + a·t = 15 m/s + 2.5 m/s² · 10 s = 40 m/s
        
        Current world state:
        {self._format_world_model(world_model)}
        
        Task: {task}
        
        Think step by step using equations and symbols. Respond in this format:
        
        <thinking>
        [Your symbolic calculations and equations]
        </thinking>
        
        <answer>
        [Your final answer/explanation based on the calculations]
        </answer>
        """
        
        # Get response from LLM
        response = self.llm.generate(prompt)
        
        # Extract the thinking and answer parts
        thinking = self._extract_between(response, "<thinking>", "</thinking>")
        answer = self._extract_between(response, "<answer>", "</answer>")
        
        return {
            "paradigm": "chunked_symbolism",
            "thinking": thinking.strip(),
            "answer": answer.strip(),
            "full_response": response
        }
    
    def _expert_lexicon_reason(self, task: str, world_model: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform reasoning using the Expert Lexicon paradigm.
        
        This paradigm uses domain-specific shorthand or acronyms that
        pack complex meaning efficiently.
        
        Args:
            task: The reasoning task/query
            world_model: Current state of the world
            
        Returns:
            Reasoning result in Expert Lexicon format
        """
        # Create prompt for expert lexicon
        prompt = f"""
        You are an AI reasoning using the Sketch-of-Thought (SoT) Expert Lexicon paradigm.
        
        In Expert Lexicon, you use domain-specific shorthand and abbreviations.
        For example: Pt w/ STEMI -> MONA (Morphine, O2, Nitrates, Aspirin)
        
        Current world state:
        {self._format_world_model(world_model)}
        
        Task: {task}
        
        Think using domain expert shorthand. Respond in this format:
        
        <thinking>
        [Your expert shorthand reasoning]
        </thinking>
        
        <answer>
        [Your final answer/explanation based on the expert reasoning]
        </answer>
        """
        
        # Get response from LLM
        response = self.llm.generate(prompt)
        
        # Extract the thinking and answer parts
        thinking = self._extract_between(response, "<thinking>", "</thinking>")
        answer = self._extract_between(response, "<answer>", "</answer>")
        
        return {
            "paradigm": "expert_lexicon",
            "thinking": thinking.strip(),
            "answer": answer.strip(),
            "full_response": response
        }
    
    def _default_reason(self, task: str, world_model: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform reasoning using a standard approach when no specific paradigm fits.
        
        Args:
            task: The reasoning task/query
            world_model: Current state of the world
            
        Returns:
            Reasoning result in default format
        """
        # Create prompt for default reasoning
        prompt = f"""
        You are an AI assistant tasked with answering a question or solving a problem.
        
        Current world state:
        {self._format_world_model(world_model)}
        
        Task: {task}
        
        Think step by step, then provide your answer.
        
        <thinking>
        [Your step-by-step reasoning]
        </thinking>
        
        <answer>
        [Your final answer/explanation]
        </answer>
        """
        
        # Get response from LLM
        response = self.llm.generate(prompt)
        
        # Extract the thinking and answer parts
        thinking = self._extract_between(response, "<thinking>", "</thinking>")
        answer = self._extract_between(response, "<answer>", "</answer>")
        
        return {
            "paradigm": "default",
            "thinking": thinking.strip(),
            "answer": answer.strip(),
            "full_response": response
        }
    
    def reason(self, task: str, world_model: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform reasoning on a task using the appropriate SoT paradigm.
        
        Args:
            task: The reasoning task/query
            world_model: Current state of the world
            
        Returns:
            Reasoning result with paradigm-specific format
        """
        # Select the appropriate reasoning paradigm
        paradigm = self._select_paradigm(task, world_model)
        
        # Use the selected paradigm to reason
        reasoning_func = self.paradigms.get(paradigm, self.paradigms["default"])
        result = reasoning_func(task, world_model)
        
        logger.info(f"Reasoning completed using paradigm: {paradigm}")
        return result
    
    def _format_world_model(self, world_model: Dict[str, Any]) -> str:
        """
        Format the world model for inclusion in prompts.
        
        Args:
            world_model: The world model dict
            
        Returns:
            Formatted string representation
        """
        formatted = ""
        for key, value in world_model.items():
            if isinstance(value, dict):
                sub_items = ", ".join([f"{k}: {v}" for k, v in value.items()])
                formatted += f"{key}: {{{sub_items}}}\n"
            else:
                formatted += f"{key}: {value}\n"
        return formatted
    
    @staticmethod
    def _extract_between(text: str, start_marker: str, end_marker: str) -> str:
        """
        Extract text between two markers.
        
        Args:
            text: The text to search in
            start_marker: The starting marker
            end_marker: The ending marker
            
        Returns:
            Extracted text between markers, or empty string if not found
        """
        try:
            start_idx = text.find(start_marker)
            if start_idx == -1:
                return ""
            start_idx += len(start_marker)
            
            end_idx = text.find(end_marker, start_idx)
            if end_idx == -1:
                return text[start_idx:]
            
            return text[start_idx:end_idx]
        except Exception as e:
            logger.error(f"Error extracting text between {start_marker} and {end_marker}: {str(e)}")
            return ""
