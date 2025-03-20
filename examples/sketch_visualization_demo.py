#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Sketch Visualization Demo

Demonstrates the visualization capabilities for Sketch-of-Thought reasoning.
"""

import os
import sys
from pathlib import Path
import matplotlib.pyplot as plt

# Add the src directory to the path for imports
project_dir = Path(__file__).parent.parent.absolute()
sys.path.append(str(project_dir))

from src.visualization.sketch_renderer import SketchRenderer

def main():
    # Create output directory for visualizations
    output_dir = project_dir / "examples" / "output"
    output_dir.mkdir(exist_ok=True)
    
    # Initialize the sketch renderer
    renderer = SketchRenderer(str(output_dir))
    
    print("=== Sketch-of-Thought Visualization Demo ===\n")
    
    # Example 1: Conceptual Chain
    print("\nExample 1: Conceptual Chain Visualization\n")
    
    conceptual_chain = """
    CO2 Emissions -> Atmospheric CO2 Increase -> Greenhouse Effect Enhancement
    Greenhouse Effect Enhancement -> Global Temperature Rise -> Ocean Temperature Increase
    Ocean Temperature Increase -> Decreased CO2 Solubility -> Reduced Ocean CO2 Absorption
    Atmospheric CO2 Increase -> Ocean CO2 Absorption -> Carbonic Acid Formation
    Carbonic Acid Formation -> Hydrogen Ion Release -> Decreased Ocean pH
    Decreased Ocean pH -> Reduced Carbonate Availability -> Impaired Shell Formation
    Impaired Shell Formation -> Marine Ecosystem Disruption -> Biodiversity Loss
    """
    
    # Render the conceptual chain
    chain_result = renderer.render_conceptual_chain(conceptual_chain)
    print(f"Generated visualization saved to: {output_dir / 'conceptual_chain.png'}")
    
    # Example 2: Equations
    print("\nExample 2: Equation Visualization\n")
    
    equations = """
    # Calculate distance traveled
    speed = 60 km/h
    time = 2.5 h
    distance = speed * time
    distance = 60 km/h * 2.5 h
    distance = 150 km
    
    # Convert to miles
    conversion_factor = 0.621371 miles/km
    distance_miles = distance * conversion_factor
    distance_miles = 150 km * 0.621371 miles/km
    distance_miles = 93.21 miles
    """
    
    # Render the equations
    equations_result = renderer.render_equations(equations)
    print(f"Generated visualization saved to: {output_dir / 'equations.png'}")
    
    # Example 3: Thought Tree
    print("\nExample 3: Thought Tree Visualization\n")
    
    thoughts = [
        {"id": "root", "text": "Analyze acute myocardial infarction (AMI) treatment", "parent_id": None},
        {"id": "assess", "text": "Initial assessment and diagnosis", "parent_id": "root"},
        {"id": "immediate", "text": "Immediate interventions", "parent_id": "root"},
        {"id": "treatment", "text": "Treatment options", "parent_id": "root"},
        {"id": "followup", "text": "Follow-up care", "parent_id": "root"},
        
        {"id": "assess1", "text": "ECG within 10 minutes", "parent_id": "assess"},
        {"id": "assess2", "text": "Cardiac biomarkers", "parent_id": "assess"},
        
        {"id": "immediate1", "text": "Oxygen therapy if needed", "parent_id": "immediate"},
        {"id": "immediate2", "text": "Aspirin 162-325mg", "parent_id": "immediate"},
        {"id": "immediate3", "text": "Nitroglycerin for chest pain", "parent_id": "immediate"},
        {"id": "immediate4", "text": "Morphine for severe pain", "parent_id": "immediate"},
        
        {"id": "treatment1", "text": "Reperfusion therapy", "parent_id": "treatment"},
        {"id": "treatment2", "text": "Antiplatelet therapy", "parent_id": "treatment"},
        {"id": "treatment3", "text": "Anticoagulation", "parent_id": "treatment"},
        
        {"id": "treatment1a", "text": "PCI (preferred if available)", "parent_id": "treatment1"},
        {"id": "treatment1b", "text": "Fibrinolysis if PCI delayed", "parent_id": "treatment1"},
        
        {"id": "followup1", "text": "Secondary prevention", "parent_id": "followup"},
        {"id": "followup2", "text": "Cardiac rehabilitation", "parent_id": "followup"},
        
        {"id": "followup1a", "text": "Statins", "parent_id": "followup1"},
        {"id": "followup1b", "text": "Beta-blockers", "parent_id": "followup1"},
        {"id": "followup1c", "text": "ACE inhibitors/ARBs", "parent_id": "followup1"},
    ]
    
    # Render the thought tree
    tree_result = renderer.render_thought_tree(thoughts)
    print(f"Generated visualization saved to: {output_dir / 'thought_tree.png'}")
    
    print("\n=== Demo Complete ===\n")
    print(f"All visualizations saved to: {output_dir}")

if __name__ == "__main__":
    main()
