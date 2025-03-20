#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Sketch-of-Thought AI Agent Demo

Demonstrates the capabilities of the SoT AI Agent with instruction following.
"""

import os
import sys
import time
import logging
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Add the src directory to the path for imports
project_dir = Path(__file__).parent.parent.absolute()
sys.path.append(str(project_dir))

from src.agent.core import SoTAgent
from src.agent.instruction_following import InstructionProcessor, InstructionSet

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def parse_args():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(description="SoT AI Agent Demo")
    parser.add_argument(
        "--mode",
        type=str,
        default="interactive",
        choices=["interactive", "demo", "instructions"],
        help="Demo mode"
    )
    return parser.parse_args()

def run_interactive_demo():
    """
    Run the agent in interactive mode.
    """
    agent = SoTAgent()
    print("\n=== Sketch-of-Thought AI Agent Interactive Demo ===\n")
    print("Type 'exit' to quit.\n")
    
    while True:
        try:
            query = input("\n> ")
            if query.lower() in ["exit", "quit"]:
                break
            
            print("\nProcessing...")
            start_time = time.time()
            
            # Run the agent cycle
            result = agent.run_once(query)
            
            # Display the output
            processing_time = time.time() - start_time
            print(f"\n[Processed in {processing_time:.2f} seconds]")
            
            if "output" in result and "text" in result["output"]:
                print(f"\nAgent: {result['output']['text']}")
                
                # Display reasoning sketch
                if "reasoning_sketch" in result["output"]:
                    print(f"\nReasoning Sketch:\n{result['output']['reasoning_sketch']}")
                
                # Display visualization if available
                if "visualization" in result["output"]:
                    vis_type = result["output"]["visualization"]["type"]
                    print(f"\n[{vis_type} visualization available]")
                    print(result["output"]["visualization"]["content"])
            else:
                print(f"\nAgent: {result}")
        
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            logger.error(f"Error in interactive demo: {str(e)}")
            print(f"Error: {str(e)}")

def run_scripted_demo():
    """
    Run a scripted demonstration of the agent's capabilities.
    """
    agent = SoTAgent()
    print("\n=== Sketch-of-Thought AI Agent Scripted Demo ===\n")
    
    # Demo queries showcasing different reasoning paradigms
    demo_queries = [
        # Conceptual chaining example
        "How does increased CO2 in the atmosphere relate to ocean acidification?",
        
        # Chunked symbolism example
        "If a car travels at 60 km/h for 2.5 hours, how far will it go?",
        
        # Expert lexicon example
        "What's the typical treatment protocol for a patient presenting with acute myocardial infarction?"
    ]
    
    for i, query in enumerate(demo_queries, 1):
        print(f"\n\n=== Demo Query {i}: {query} ===\n")
        print("Processing...")
        start_time = time.time()
        
        # Run the agent cycle
        result = agent.run_once(query)
        
        # Display the output
        processing_time = time.time() - start_time
        print(f"\n[Processed in {processing_time:.2f} seconds]")
        
        if "output" in result and "text" in result["output"]:
            print(f"\nAgent: {result['output']['text']}")
            
            # Display reasoning sketch
            if "reasoning_sketch" in result["output"]:
                print(f"\nReasoning Sketch:\n{result['output']['reasoning_sketch']}")
            
            # Display visualization if available
            if "visualization" in result["output"]:
                vis_type = result["output"]["visualization"]["type"]
                print(f"\n[{vis_type} visualization available]")
                print(result["output"]["visualization"]["content"])
        else:
            print(f"\nAgent: {result}")
        
        # Pause between demos
        if i < len(demo_queries):
            print("\nContinuing to next demo in 3 seconds...")
            time.sleep(3)

def run_instruction_following_demo():
    """
    Run a demonstration of the instruction following capabilities.
    """
    agent = SoTAgent()
    instruction_processor = InstructionProcessor(agent.llm)
    instruction_set = InstructionSet()
    
    print("\n=== Instruction Following Demonstration ===\n")
    
    # Add some sample instructions
    instructions = [
        "Analyze the temperature data from the past 24 hours and identify any anomalies",
        "Generate a report on the current system status, including all sensor readings",
        "Create a prediction model for future temperature trends based on historical data"
    ]
    
    # Add instructions to the set
    for i, instr in enumerate(instructions):
        priority = len(instructions) - i  # Higher priority for earlier instructions
        instruction_set.add_instruction(instr, priority=priority)
    
    # Process each instruction
    while not instruction_set.all_completed():
        next_instruction = instruction_set.get_next_instruction()
        if not next_instruction:
            print("No more instructions to process")
            break
        
        print(f"\n\n=== Processing Instruction: {next_instruction['text']} ===\n")
        print("Analyzing instruction...")
        
        # Process the instruction
        result = instruction_processor.process_instruction(next_instruction['text'])
        
        # Display the results
        print("\nInstruction Analysis:")
        print(result['analysis'])
        
        print("\nResponse:")
        print(result['response'])
        
        print("\nVerification:")
        print(result['verification'])
        
        # Mark as completed
        instruction_set.mark_current_completed()
        
        # Pause between instructions
        if not instruction_set.all_completed():
            print("\nContinuing to next instruction in 3 seconds...")
            time.sleep(3)
    
    print("\n\nAll instructions completed.")

def main():
    """
    Main entry point for the demo.
    """
    args = parse_args()
    
    if args.mode == "interactive":
        run_interactive_demo()
    elif args.mode == "demo":
        run_scripted_demo()
    elif args.mode == "instructions":
        run_instruction_following_demo()

if __name__ == "__main__":
    main()
