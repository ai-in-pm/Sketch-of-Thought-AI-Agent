#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Instruction Following Mock Test

Demonstrates the instruction following capabilities with mock data.
"""

import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import json

# Add the src directory to the path for imports
project_dir = Path(__file__).parent.parent.absolute()
sys.path.append(str(project_dir))

# Import required modules
from src.agent.instruction_following import InstructionProcessor, InstructionSet

class MockLLMInterface:
    """
    Mock LLM interface for testing
    """
    
    def __init__(self):
        self.mock_responses = {
            "analysis": json.dumps({
                "primary_objectives": ["Generate a list of 5 alternative energy sources"],
                "constraints": ["Must include advantages for each source"],
                "methodologies": ["None specified"],
                "output_format": ["List format implied"]
            }),
            "execution": """
# Alternative Energy Sources and Their Advantages

1. **Solar Energy**
   - Renewable and inexhaustible
   - No greenhouse gas emissions during operation
   - Low maintenance costs after initial installation
   - Can be deployed at various scales (residential to utility)

2. **Wind Energy**
   - Renewable resource with no fuel costs
   - One of the lowest-priced renewable energy technologies
   - Creates jobs in manufacturing, installation, and maintenance
   - Can be built on existing farms or ranches

3. **Geothermal Energy**
   - Constant output regardless of weather conditions
   - Very small land footprint per unit of energy
   - Lower emissions compared to fossil fuels
   - Provides reliable baseload power

4. **Hydroelectric Power**
   - High efficiency (>90% in converting energy to electricity)
   - Long lifespan of facilities (50-100 years)
   - Reservoirs can provide flood control and water supply
   - Quick response to electricity demand peaks

5. **Hydrogen Fuel Cells**
   - Zero emissions (water is the only byproduct)
   - High energy efficiency
   - Quiet operation
   - Potential for energy storage to balance intermittent renewables
""",
            "verification": json.dumps({
                "result": True,
                "explanation": "The response fulfills all requirements: it provides exactly 5 alternative energy sources with clear advantages listed for each. The format is a well-structured list as implied by the instruction."
            })
        }
    
    def generate(self, prompt: str) -> str:
        """
        Return mock response based on prompt content
        """
        if "analyze the following instruction" in prompt.lower():
            return self.mock_responses["analysis"]
        elif "execute the instruction" in prompt.lower():
            return self.mock_responses["execution"]
        elif "verify if the response" in prompt.lower():
            return self.mock_responses["verification"]
        else:
            return "Default mock response"

def main():
    # Initialize components
    mock_llm = MockLLMInterface()
    instruction_processor = InstructionProcessor(mock_llm)
    instruction_set = InstructionSet()
    
    print("=== Instruction Following Mock Test ===\n")
    
    # Test instruction
    test_instruction = "Create a list of 5 alternative energy sources and their main advantages"
    
    # Add to instruction set
    instruction_set.add_instruction(test_instruction, priority=1)
    
    # Process the next instruction
    next_instruction = instruction_set.get_next_instruction()
    if next_instruction:
        print(f"Processing instruction: {next_instruction['text']}\n")
        
        # Process the instruction
        result = instruction_processor.process_instruction(next_instruction['text'])
        
        # Display the results
        print("\nInstruction Analysis:")
        print(json.dumps(result['analysis'], indent=2))
        
        print("\nResponse:")
        print(result['response'])
        
        print("\nVerification:")
        print(json.dumps(result['verification'], indent=2))
        
        # Mark as completed
        instruction_set.mark_current_completed()
        print(f"\nInstruction completed: {instruction_set.all_completed()}")
    
    print("\n=== Mock Test Complete ===\n")

if __name__ == "__main__":
    main()
