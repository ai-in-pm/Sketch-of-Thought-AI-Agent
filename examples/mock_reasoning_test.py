#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Mock Reasoning Test

Tests the SoT reasoning paradigms with mock responses.
"""

import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import json

# Add the src directory to the path for imports
project_dir = Path(__file__).parent.parent.absolute()
sys.path.append(str(project_dir))

# Import visualization tools
from src.visualization.sketch_renderer import SketchRenderer
from src.visualization.outputs import OutputGenerator

# Mock data for testing
MOCK_CONCEPTUAL_CHAIN = """
Conceptual Chain Reasoning:

CO2 Emissions -> Atmospheric CO2 Increase -> Greenhouse Effect Enhancement
Greenhouse Effect Enhancement -> Global Temperature Rise -> Ocean Temperature Increase
Ocean Temperature Increase -> Decreased CO2 Solubility -> Reduced Ocean CO2 Absorption
Atmospheric CO2 Increase -> Ocean CO2 Absorption -> Carbonic Acid Formation
Carbonic Acid Formation -> Hydrogen Ion Release -> Decreased Ocean pH
Decreased Ocean pH -> Reduced Carbonate Availability -> Impaired Shell Formation
"""

MOCK_CHUNKED_SYMBOLISM = """
Chunked Symbolism Reasoning:

# Define variables
speed = 60 km/h
time = 2.5 h

# Calculate distance
distance = speed * time
distance = 60 km/h * 2.5 h
distance = 150 km

# Convert to miles
conversion_factor = 0.621371 miles/km
distance_miles = distance * conversion_factor
distance_miles = 150 km * 0.621371 miles/km
distance_miles = 93.21 miles
"""

MOCK_EXPERT_LEXICON = """
Expert Lexicon Reasoning:

Acute Myocardial Infarction (AMI) Treatment Protocol:
1. Initial assessment - ECG within 10 minutes, cardiac biomarkers (troponin, CK-MB)
2. Immediate interventions - Aspirin (162-325mg), Oxygen if saturation < 90%, Nitroglycerin for pain
3. Reperfusion strategy - Primary PCI if available within 90 minutes, otherwise fibrinolysis
4. Anticoagulation - Heparin or low molecular weight heparin
5. Secondary prevention - Statins, Beta-blockers, ACE inhibitors/ARBs
"""

class MockSoTReasoner:
    """
    Mock SoT Reasoner for testing
    """
    
    def __init__(self):
        pass
    
    def reason(self, task: str, world_model: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Mock reasoning based on task keywords
        """
        world_model = world_model or {}
        
        # Choose reasoning paradigm based on task keywords
        if any(kw in task.lower() for kw in ["co2", "carbon", "ocean", "climate", "temperature"]):
            return {
                "paradigm": "conceptual_chaining",
                "thinking": MOCK_CONCEPTUAL_CHAIN,
                "answer": ("Increased CO2 in the atmosphere leads to ocean acidification through a chain "
                          "of processes. When CO2 is absorbed by the ocean, it forms carbonic acid, which "
                          "releases hydrogen ions, decreasing the ocean's pH. This acidification reduces "
                          "carbonate availability, making it difficult for marine organisms to form shells "
                          "and skeletons, disrupting marine ecosystems.")
            }
        
        elif any(kw in task.lower() for kw in ["calculate", "distance", "speed", "time", "equation"]):
            return {
                "paradigm": "chunked_symbolism",
                "thinking": MOCK_CHUNKED_SYMBOLISM,
                "answer": ("If a car travels at 60 km/h for 2.5 hours, it will cover a distance of 150 km "
                          "(calculated as speed × time = 60 km/h × 2.5 h = 150 km). Converting to miles, "
                          "this is approximately 93.21 miles.")
            }
        
        elif any(kw in task.lower() for kw in ["medical", "treatment", "protocol", "heart", "infarction"]):
            return {
                "paradigm": "expert_lexicon",
                "thinking": MOCK_EXPERT_LEXICON,
                "answer": ("The typical treatment protocol for acute myocardial infarction includes: "
                          "immediate assessment with ECG and cardiac biomarkers; administration of aspirin "
                          "and oxygen; timely reperfusion via PCI or fibrinolysis; anticoagulation; and "
                          "secondary prevention with medications like statins and beta-blockers. This "
                          "protocol aims to restore blood flow, limit infarct size, and prevent complications.")
            }
        
        else:
            # Default to conceptual chaining
            return {
                "paradigm": "conceptual_chaining",
                "thinking": "Default reasoning approach with limited context\nA -> B -> C",
                "answer": "I've analyzed your query using a conceptual chain approach, but more specific information may yield better results."
            }

def main():
    # Initialize components
    reasoner = MockSoTReasoner()
    output_generator = OutputGenerator()
    renderer = SketchRenderer(str(project_dir / "examples" / "output"))
    
    print("=== Mock SoT AI Agent Reasoning Test ===\n")
    
    # Test queries for different paradigms
    test_queries = [
        "How does increased CO2 in the atmosphere relate to ocean acidification?",
        "If a car travels at 60 km/h for 2.5 hours, how far will it go?",
        "What's the typical treatment protocol for a patient presenting with acute myocardial infarction?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n[Query {i}]: {query}\n")
        
        # Get reasoning result
        reason_result = reasoner.reason(query)
        paradigm = reason_result.get("paradigm")
        
        print(f"Selected paradigm: {paradigm}\n")
        print(f"Answer: {reason_result.get('answer')}\n")
        print(f"Reasoning sketch:\n{reason_result.get('thinking')}\n")
        
        # Generate output with visualization
        output = output_generator.generate_output(reason_result)
        
        # Generate visualization
        viz_result = renderer.render_sketch(reason_result.get('thinking', ''))
        print(f"Generated visualization: {viz_result['type']}")
        
        if viz_result['type'] != 'text':
            viz_path = f"output/{paradigm}_viz.png"
            print(f"Visualization saved to: {viz_path}\n")
        
        print("-" * 80)
    
    print("\n=== Mock Reasoning Test Complete ===\n")
    print(f"All visualizations saved to: {project_dir / 'examples' / 'output'}\n")

if __name__ == "__main__":
    main()
