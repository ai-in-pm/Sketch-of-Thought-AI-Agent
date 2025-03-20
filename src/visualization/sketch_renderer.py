#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Sketch Renderer

Generates visual representations of reasoning sketches.
"""

import logging
from typing import Any, Dict, List, Optional, Tuple, Union
from pathlib import Path
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import FancyArrowPatch
import io
import base64
import re

# Setup logging
logger = logging.getLogger(__name__)

class SketchRenderer:
    """
    Sketch Renderer
    
    Renders visual representations of reasoning sketches to enhance
    understanding and explainability of the agent's reasoning process.
    """
    
    def __init__(self, output_dir: Optional[str] = None):
        """
        Initialize the Sketch Renderer.
        
        Args:
            output_dir: Optional directory to save rendered sketches
        """
        self.output_dir = output_dir
        if output_dir:
            Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        logger.info("SketchRenderer initialized")
    
    def render_conceptual_chain(self, chain_text: str) -> Dict[str, Any]:
        """
        Render a conceptual chain diagram from text.
        
        Args:
            chain_text: Text containing conceptual chains (using -> format)
            
        Returns:
            Dictionary with rendering information
        """
        try:
            # Extract chains
            chains = []
            for line in chain_text.split("\n"):
                if "->" in line:
                    chain = [item.strip() for item in line.split("->")]
                    if len(chain) > 1:
                        chains.append(chain)
            
            if not chains:
                logger.warning("No valid chains found in input text")
                return {
                    "type": "text",
                    "format": "text",
                    "content": chain_text
                }
            
            # Create a directed graph
            G = nx.DiGraph()
            
            # Add nodes and edges
            all_nodes = set()
            for chain in chains:
                for node in chain:
                    all_nodes.add(node)
                
                for i in range(len(chain) - 1):
                    G.add_edge(chain[i], chain[i+1])
            
            # Draw the graph
            plt.figure(figsize=(10, 8))
            pos = nx.spring_layout(G, seed=42)  # For reproducibility
            
            # Draw nodes
            nx.draw_networkx_nodes(G, pos, node_size=2000, node_color="lightblue", alpha=0.8)
            
            # Draw edges
            nx.draw_networkx_edges(G, pos, width=2, arrowsize=20, alpha=0.7)
            
            # Draw labels
            nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif")
            
            # Set title
            plt.title("Conceptual Chain Visualization")
            plt.axis("off")
            
            # Save to buffer
            buffer = io.BytesIO()
            plt.savefig(buffer, format="png", dpi=300, bbox_inches="tight")
            buffer.seek(0)
            
            # Save to file if output_dir is specified
            if self.output_dir:
                plt.savefig(
                    Path(self.output_dir) / "conceptual_chain.png", 
                    format="png", 
                    dpi=300, 
                    bbox_inches="tight"
                )
            
            # Encode as base64
            image_data = base64.b64encode(buffer.read()).decode("utf-8")
            plt.close()
            
            return {
                "type": "conceptual_chain",
                "format": "image/png;base64",
                "content": image_data,
                "nodes": list(all_nodes),
                "edges": list(G.edges())
            }
        
        except Exception as e:
            logger.error(f"Error rendering conceptual chain: {str(e)}")
            return {
                "type": "text",
                "format": "text",
                "content": chain_text,
                "error": str(e)
            }
    
    def render_thought_tree(self, thoughts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Render a tree visualization of thoughts and sub-thoughts.
        
        Args:
            thoughts: List of thought objects with parent-child relationships
            
        Returns:
            Dictionary with rendering information
        """
        try:
            if not thoughts:
                return {
                    "type": "text",
                    "format": "text",
                    "content": "No thoughts to visualize"
                }
            
            # Create a directed graph
            G = nx.DiGraph()
            
            # Process nodes and edges
            for thought in thoughts:
                thought_id = thought.get("id", str(thoughts.index(thought)))
                thought_text = thought.get("text", "")
                parent_id = thought.get("parent_id")
                
                # Truncate long thought texts
                if len(thought_text) > 30:
                    thought_text = thought_text[:27] + "..."
                
                # Add node
                G.add_node(thought_id, text=thought_text)
                
                # Add edge if parent exists
                if parent_id is not None:
                    G.add_edge(parent_id, thought_id)
            
            # Draw the graph
            plt.figure(figsize=(12, 10))
            
            # Use a tree layout
            pos = nx.nx_agraph.graphviz_layout(G, prog="dot") if nx.is_tree(G) else nx.spring_layout(G)
            
            # Draw nodes
            nx.draw_networkx_nodes(G, pos, node_size=2000, node_color="lightgreen", alpha=0.8)
            
            # Draw edges
            nx.draw_networkx_edges(G, pos, width=2, arrowsize=20, alpha=0.7)
            
            # Draw labels
            labels = {node: G.nodes[node]["text"] for node in G.nodes()}
            nx.draw_networkx_labels(G, pos, labels=labels, font_size=8, font_family="sans-serif")
            
            # Set title
            plt.title("Thought Tree Visualization")
            plt.axis("off")
            
            # Save to buffer
            buffer = io.BytesIO()
            plt.savefig(buffer, format="png", dpi=300, bbox_inches="tight")
            buffer.seek(0)
            
            # Save to file if output_dir is specified
            if self.output_dir:
                plt.savefig(
                    Path(self.output_dir) / "thought_tree.png", 
                    format="png", 
                    dpi=300, 
                    bbox_inches="tight"
                )
            
            # Encode as base64
            image_data = base64.b64encode(buffer.read()).decode("utf-8")
            plt.close()
            
            return {
                "type": "thought_tree",
                "format": "image/png;base64",
                "content": image_data,
                "nodes": list(G.nodes()),
                "edges": list(G.edges())
            }
        
        except Exception as e:
            logger.error(f"Error rendering thought tree: {str(e)}")
            return {
                "type": "text",
                "format": "text",
                "content": str(thoughts),
                "error": str(e)
            }
    
    def render_equations(self, equations_text: str) -> Dict[str, Any]:
        """
        Render mathematical equations.
        
        Args:
            equations_text: Text containing equations
            
        Returns:
            Dictionary with rendering information
        """
        try:
            # Extract equations (lines containing = sign)
            equations = []
            for line in equations_text.split("\n"):
                if "=" in line and not line.strip().startswith("#"):
                    equations.append(line.strip())
            
            if not equations:
                return {
                    "type": "text",
                    "format": "text",
                    "content": equations_text
                }
            
            # Format equations for display
            formatted_equations = []
            for i, eq in enumerate(equations):
                # Add equation number
                formatted_eq = f"({i+1})\t{eq}"
                formatted_equations.append(formatted_eq)
            
            # Create a simple visualization
            plt.figure(figsize=(10, len(equations) * 0.5 + 2))
            plt.text(0.1, 0.5, "\n".join(formatted_equations), 
                    fontsize=12, family="monospace",
                    verticalalignment="center")
            plt.axis("off")
            plt.title("Equation Sketch")
            
            # Save to buffer
            buffer = io.BytesIO()
            plt.savefig(buffer, format="png", dpi=300, bbox_inches="tight")
            buffer.seek(0)
            
            # Save to file if output_dir is specified
            if self.output_dir:
                plt.savefig(
                    Path(self.output_dir) / "equations.png", 
                    format="png", 
                    dpi=300, 
                    bbox_inches="tight"
                )
            
            # Encode as base64
            image_data = base64.b64encode(buffer.read()).decode("utf-8")
            plt.close()
            
            return {
                "type": "equations",
                "format": "image/png;base64",
                "content": image_data,
                "equations": equations
            }
        
        except Exception as e:
            logger.error(f"Error rendering equations: {str(e)}")
            return {
                "type": "text",
                "format": "text",
                "content": equations_text,
                "error": str(e)
            }
    
    def detect_sketch_type(self, text: str) -> str:
        """
        Detect the type of sketch based on content.
        
        Args:
            text: The text to analyze
            
        Returns:
            Detected sketch type
        """
        # Check for conceptual chains
        if "->" in text:
            chain_count = len(re.findall(r'\s*->\s*', text))
            if chain_count >= 2:  # At least one complete chain
                return "conceptual_chain"
        
        # Check for equations
        equation_count = len([line for line in text.split("\n") 
                            if "=" in line and not line.strip().startswith("#")])
        if equation_count >= 2:
            return "equations"
        
        # Default to text
        return "text"
    
    def render_sketch(self, sketch_text: str) -> Dict[str, Any]:
        """
        Automatically detect and render the appropriate visualization for a sketch.
        
        Args:
            sketch_text: The sketch text to visualize
            
        Returns:
            Rendering result
        """
        sketch_type = self.detect_sketch_type(sketch_text)
        
        if sketch_type == "conceptual_chain":
            return self.render_conceptual_chain(sketch_text)
        elif sketch_type == "equations":
            return self.render_equations(sketch_text)
        else:
            return {
                "type": "text",
                "format": "text",
                "content": sketch_text
            }
