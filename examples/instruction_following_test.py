#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Instruction Following Test

Simple test for the instruction following module.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add the src directory to the path for imports
project_dir = Path(__file__).parent.parent.absolute()
sys.path.append(str(project_dir))

# Load environment variables
load_dotenv()

from src.models.llm import LLMInterface
from src.agent.instruction_following import InstructionProcessor, InstructionSet
import openai

def main():
    if not os.getenv('OPENAI_API_KEY'):
        print("Error: OPENAI_API_KEY not found in environment variables.")
        print("Please set your OpenAI API key in the .env file.")
        return
    
    # Initialize OpenAI client
    openai_client = openai.OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Initialize the LLM interface
    model_name = os.getenv("MODEL_NAME", "gpt-4")
    temperature = float(os.getenv("TEMPERATURE", "0.7"))
    llm = LLMInterface(
        client=openai_client,
        model_name=model_name,
        temperature=temperature
    )
    
    # Initialize the instruction processor
    instruction_processor = InstructionProcessor(llm)
    
    print("\n=== Instruction Following Test ===\n")
    
    # Simple test instruction
    test_instruction = "Create a list of 5 alternative energy sources and their main advantages"
    
    print(f"Processing instruction: {test_instruction}\n")
    
    # Process the instruction
    result = instruction_processor.process_instruction(test_instruction)
    
    # Display the results
    print("\nInstruction Analysis:")
    print(result['analysis'])
    
    print("\nResponse:")
    print(result['response'])
    
    print("\nVerification:")
    print(result['verification'])
    
    print("\n=== Test Complete ===\n")

if __name__ == "__main__":
    main()
