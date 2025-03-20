#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Instruction Following Module

Integrates instruction following capabilities into the AI agent.
This module adapts the instruction-following framework from:
https://github.com/ai-in-pm/Instruction-Following-for-AI-Agents
"""

import os
import sys
import logging
from typing import Any, Dict, List, Optional, Union
import json

from src.models.llm import LLMInterface

# Setup logging
logger = logging.getLogger(__name__)

class InstructionProcessor:
    """
    Instruction Processor
    
    Processes and follows instructions given to the agent, using structured
    instruction following techniques to ensure consistent execution.
    """
    
    def __init__(self, llm: LLMInterface):
        """
        Initialize the Instruction Processor.
        
        Args:
            llm: LLM interface for processing instructions
        """
        self.llm = llm
        
        # Load instruction following prompts and templates
        self.prompts = self._load_instruction_templates()
        
        logger.info("InstructionProcessor initialized")
    
    def _load_instruction_templates(self) -> Dict[str, str]:
        """
        Load instruction following templates.
        
        Returns:
            Dictionary of prompt templates
        """
        # Default templates
        templates = {
            "instruction_analysis": """
            You are an AI assistant dedicated to accurately following instructions.
            Your task is to analyze the following instruction:
            
            INSTRUCTION: {instruction}
            
            Break down this instruction into:
            1. Primary objective(s)
            2. Constraints or requirements
            3. Any specific methodologies to follow
            4. Expected output format
            
            Respond in JSON format with these components.
            """,
            
            "instruction_execution": """
            You are an AI assistant following instructions precisely.
            
            INSTRUCTION: {instruction}
            
            INSTRUCTION ANALYSIS: {analysis}
            
            Based on this analysis, execute the instruction exactly as specified.
            Ensure your response adheres to all constraints and output formats.
            """,
            
            "instruction_verification": """
            You are an AI assistant verifying instruction execution.
            
            ORIGINAL INSTRUCTION: {instruction}
            INSTRUCTION ANALYSIS: {analysis}
            GENERATED RESPONSE: {response}
            
            Verify if the response correctly follows the instruction.
            Check against each component of the analysis.
            If there are discrepancies, explain them.
            
            Respond in JSON format with a verification result (true/false) and explanation.
            """
        }
        
        # In a production system, we would load these from actual files
        # included in the cloned repository
        
        return templates
    
    def process_instruction(self, instruction: str) -> Dict[str, Any]:
        """
        Process an instruction through the three-step framework:
        1. Analyze the instruction
        2. Execute the instruction
        3. Verify the execution
        
        Args:
            instruction: The instruction to process
            
        Returns:
            Processing result with verification
        """
        try:
            # Step 1: Analyze the instruction
            analysis_prompt = self.prompts["instruction_analysis"].format(
                instruction=instruction
            )
            
            analysis_response = self.llm.generate(analysis_prompt)
            analysis = self._extract_json(analysis_response)
            
            if not analysis:
                logger.warning("Failed to parse instruction analysis as JSON")
                analysis = {"raw_analysis": analysis_response}
            
            logger.info(f"Analyzed instruction with {len(analysis)} components")
            
            # Step 2: Execute the instruction
            execution_prompt = self.prompts["instruction_execution"].format(
                instruction=instruction,
                analysis=json.dumps(analysis, indent=2)
            )
            
            execution_response = self.llm.generate(execution_prompt)
            logger.info("Generated instruction execution response")
            
            # Step 3: Verify the execution
            verification_prompt = self.prompts["instruction_verification"].format(
                instruction=instruction,
                analysis=json.dumps(analysis, indent=2),
                response=execution_response
            )
            
            verification_response = self.llm.generate(verification_prompt)
            verification = self._extract_json(verification_response)
            
            if not verification:
                logger.warning("Failed to parse verification as JSON")
                verification = {"raw_verification": verification_response}
            
            # Combine results
            result = {
                "instruction": instruction,
                "analysis": analysis,
                "response": execution_response,
                "verification": verification
            }
            
            return result
        
        except Exception as e:
            logger.error(f"Error processing instruction: {str(e)}")
            return {
                "instruction": instruction,
                "error": str(e)
            }
    
    def _extract_json(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Extract and parse JSON from a text response.
        
        Args:
            text: Text that may contain JSON
            
        Returns:
            Parsed JSON object or None if parsing fails
        """
        try:
            # Try to find JSON-like content
            start_idx = text.find('{')
            end_idx = text.rfind('}')
            
            if start_idx >= 0 and end_idx >= 0:
                json_str = text[start_idx:end_idx+1]
                return json.loads(json_str)
            
            # Try the whole text as JSON
            return json.loads(text)
        
        except json.JSONDecodeError:
            logger.debug("Failed to parse as JSON")
            return None


class InstructionSet:
    """
    Instruction Set
    
    Manages a collection of instructions that the agent can follow,
    including their priorities, dependencies, and execution status.
    """
    
    def __init__(self):
        """
        Initialize an empty Instruction Set.
        """
        self.instructions = []
        self.current_instruction_index = -1
        
        logger.info("InstructionSet initialized")
    
    def add_instruction(self, instruction: str, priority: int = 0, dependencies: List[int] = None) -> int:
        """
        Add an instruction to the set.
        
        Args:
            instruction: The instruction text
            priority: Priority level (higher numbers = higher priority)
            dependencies: List of instruction indices that must be completed first
            
        Returns:
            Index of the added instruction
        """
        instruction_obj = {
            "text": instruction,
            "priority": priority,
            "dependencies": dependencies or [],
            "completed": False,
            "index": len(self.instructions)
        }
        
        self.instructions.append(instruction_obj)
        logger.info(f"Added instruction with index {instruction_obj['index']}")
        
        # Sort instructions by priority (highest first)
        self.instructions.sort(key=lambda x: x["priority"], reverse=True)
        
        return instruction_obj["index"]
    
    def get_next_instruction(self) -> Optional[Dict[str, Any]]:
        """
        Get the next instruction to execute based on priority and dependencies.
        
        Returns:
            The next instruction object or None if all are completed
        """
        for instr in self.instructions:
            # Skip completed instructions
            if instr["completed"]:
                continue
            
            # Check dependencies
            dependencies_met = True
            for dep_idx in instr["dependencies"]:
                # Find the dependency in the instructions list
                dependency = next((d for d in self.instructions if d["index"] == dep_idx), None)
                
                if dependency and not dependency["completed"]:
                    dependencies_met = False
                    break
            
            if dependencies_met:
                self.current_instruction_index = instr["index"]
                return instr
        
        return None
    
    def mark_current_completed(self) -> bool:
        """
        Mark the current instruction as completed.
        
        Returns:
            Success status
        """
        if self.current_instruction_index < 0:
            logger.warning("No current instruction to mark as completed")
            return False
        
        # Find the instruction with the matching index
        for instr in self.instructions:
            if instr["index"] == self.current_instruction_index:
                instr["completed"] = True
                logger.info(f"Marked instruction {self.current_instruction_index} as completed")
                self.current_instruction_index = -1
                return True
        
        logger.warning(f"Could not find instruction with index {self.current_instruction_index}")
        return False
    
    def all_completed(self) -> bool:
        """
        Check if all instructions are completed.
        
        Returns:
            True if all instructions are completed, False otherwise
        """
        return all(instr["completed"] for instr in self.instructions)
    
    def reset(self):
        """
        Reset the completion status of all instructions.
        """
        for instr in self.instructions:
            instr["completed"] = False
        
        self.current_instruction_index = -1
        logger.info("Reset all instruction completion statuses")
