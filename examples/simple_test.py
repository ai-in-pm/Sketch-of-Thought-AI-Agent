#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simple Test Script

Demonstrates the basic functionality of the SoT AI Agent.
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

from src.visualization.sketch_renderer import SketchRenderer

def simple_test():
    print("=== Simple Test of SoT AI Agent Components ===\n")
    
    # Test visualization components
    renderer = SketchRenderer()
    
    # Simple conceptual chain example
    chain = "A -> B -> C\nD -> E -> F"
    print("Testing conceptual chain rendering...")
    result = renderer.detect_sketch_type(chain)
    print(f"Detected sketch type: {result}")
    
    # Test equation rendering
    equations = "x = 5\ny = 10\nz = x + y"
    print("\nTesting equation detection...")
    result = renderer.detect_sketch_type(equations)
    print(f"Detected sketch type: {result}")
    
    print("\n=== Component Tests Completed Successfully ===\n")
    
    return True

if __name__ == "__main__":
    simple_test()
