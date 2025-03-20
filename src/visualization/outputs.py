#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Output Generator

Generates structured outputs from reasoning results, including visualizations.
"""

import logging
from typing import Any, Dict, List, Optional, Union
import matplotlib.pyplot as plt
import io
import base64

# Setup logging
logger = logging.getLogger(__name__)

class OutputGenerator:
    """
    Output Generator
    
    Transforms reasoning results into structured outputs, including
    text, graphs, diagrams, equations, and step-by-step explanations.
    """
    
    def __init__(self):
        """
        Initialize the Output Generator.
        """
        logger.info("OutputGenerator initialized")
    
    def generate_output(self, reasoning_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate appropriate output from reasoning result.
        
        Args:
            reasoning_result: Result from the SoT reasoner
            
        Returns:
            Structured output with appropriate visualizations
        """
        # Extract the paradigm and answer
        paradigm = reasoning_result.get("paradigm", "default")
        answer = reasoning_result.get("answer", "")
        thinking = reasoning_result.get("thinking", "")
        
        # Prepare the base output
        output = {
            "text": answer,
            "reasoning_sketch": thinking
        }
        
        # Generate paradigm-specific visualizations
        if paradigm == "conceptual_chaining":
            visualization = self._generate_conceptual_chain_viz(thinking)
            if visualization:
                output["visualization"] = visualization
        
        elif paradigm == "chunked_symbolism":
            visualization = self._generate_equation_viz(thinking)
            if visualization:
                output["visualization"] = visualization
        
        elif paradigm == "expert_lexicon":
            # Currently no specific visualization for expert lexicon
            pass
        
        logger.info(f"Generated output for paradigm: {paradigm}")
        return output
    
    def _generate_conceptual_chain_viz(self, thinking: str) -> Optional[Dict[str, Any]]:
        """
        Generate visualization for conceptual chaining.
        
        Args:
            thinking: The conceptual chain reasoning
            
        Returns:
            Visualization data if successful, None otherwise
        """
        try:
            # Extract chains (assuming -> format)
            chains = []
            for line in thinking.split("\n"):
                if "->" in line:
                    chain = [item.strip() for item in line.split("->")]
                    if len(chain) > 1:
                        chains.append(chain)
            
            if not chains:
                return None
            
            # Generate a simple ASCII diagram for now
            # In a real implementation, this could generate a proper graph visualization
            diagram = ""
            for chain in chains:
                diagram += " -> ".join(chain) + "\n"
            
            return {
                "type": "conceptual_chain",
                "format": "ascii",
                "content": diagram
            }
        
        except Exception as e:
            logger.error(f"Error generating conceptual chain visualization: {str(e)}")
            return None
    
    def _generate_equation_viz(self, thinking: str) -> Optional[Dict[str, Any]]:
        """
        Generate visualization for equations and symbolic reasoning.
        
        Args:
            thinking: The symbolic reasoning
            
        Returns:
            Visualization data if successful, None otherwise
        """
        try:
            # Extract equations
            equations = []
            for line in thinking.split("\n"):
                if "=" in line and not line.strip().startswith("#"):
                    equations.append(line.strip())
            
            if not equations:
                return None
            
            # Format equations as LaTeX for better display
            # In a real implementation, this would render proper equation visualizations
            latex_equations = []
            for eq in equations:
                # Simple conversion to LaTeX-like format
                # A real implementation would use a proper LaTeX converter
                latex_eq = eq.replace("*", "\\cdot ")
                latex_eq = latex_eq.replace("^", "^{")
                if "^{" in latex_eq:
                    latex_eq = latex_eq.replace(" ", "} ", 1)
                latex_equations.append(latex_eq)
            
            return {
                "type": "equation",
                "format": "latex",
                "content": "\n".join(latex_equations)
            }
        
        except Exception as e:
            logger.error(f"Error generating equation visualization: {str(e)}")
            return None
    
    def generate_graph(self, data: Dict[str, List[float]], title: str = "", xlabel: str = "", ylabel: str = "") -> Optional[Dict[str, Any]]:
        """
        Generate a graph visualization from data.
        
        Args:
            data: Dictionary mapping series names to data points
            title: Graph title
            xlabel: X-axis label
            ylabel: Y-axis label
            
        Returns:
            Graph visualization data
        """
        try:
            # Create figure and axis
            fig, ax = plt.subplots(figsize=(8, 5))
            
            # Plot each data series
            for series_name, values in data.items():
                ax.plot(values, label=series_name)
            
            # Add labels and title
            if xlabel:
                ax.set_xlabel(xlabel)
            if ylabel:
                ax.set_ylabel(ylabel)
            if title:
                ax.set_title(title)
            
            # Add legend if multiple series
            if len(data) > 1:
                ax.legend()
            
            # Add grid for readability
            ax.grid(True, linestyle='--', alpha=0.7)
            
            # Save figure to a bytes buffer
            buffer = io.BytesIO()
            fig.savefig(buffer, format='png')
            buffer.seek(0)
            
            # Encode the image as base64
            image_data = base64.b64encode(buffer.read()).decode('utf-8')
            plt.close(fig)
            
            return {
                "type": "graph",
                "format": "image/png;base64",
                "content": image_data
            }
        
        except Exception as e:
            logger.error(f"Error generating graph: {str(e)}")
            return None
    
    def generate_step_by_step(self, steps: List[str]) -> Dict[str, Any]:
        """
        Generate a step-by-step explanation visualization.
        
        Args:
            steps: List of reasoning steps
            
        Returns:
            Step-by-step visualization data
        """
        try:
            formatted_steps = ""
            for i, step in enumerate(steps, 1):
                formatted_steps += f"{i}. {step}\n"
            
            return {
                "type": "step_by_step",
                "format": "text",
                "content": formatted_steps
            }
        
        except Exception as e:
            logger.error(f"Error generating step-by-step visualization: {str(e)}")
            return {
                "type": "step_by_step",
                "format": "text",
                "content": "Error generating steps."
            }
