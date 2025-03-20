#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Sketch-of-Thought AI Agent: Core Agent Implementation

This module implements the core SoT AI Agent that perceives the environment,
reasoning using Sketch-of-Thought paradigms, and acts accordingly.
"""

import os
import time
import logging
from typing import Any, Dict, List, Optional, Tuple, Union

from dotenv import load_dotenv
import openai

from reasoning.sot import SoTReasoner
from models.llm import LLMInterface
from sensors.data_manager import SensorDataManager
from visualization.outputs import OutputGenerator

# Load environment variables
load_dotenv()

# Setup logging
logger = logging.getLogger(__name__)

class SoTAgent:
    """
    Sketch-of-Thought AI Agent
    
    This agent perceives the environment through various sensors,
    processes information using efficient Sketch-of-Thought reasoning,
    and responds or acts accordingly.
    """
    
    def __init__(self):
        """
        Initialize the Sketch-of-Thought AI Agent with its components.
        """
        # Initialize OpenAI client
        self.openai_client = openai.OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Initialize components
        self.model_name = os.getenv("MODEL_NAME", "gpt-4")
        self.temperature = float(os.getenv("TEMPERATURE", "0.7"))
        
        # Initialize the LLM interface
        self.llm = LLMInterface(
            client=self.openai_client,
            model_name=self.model_name,
            temperature=self.temperature
        )
        
        # Initialize the SoT reasoner
        self.reasoner = SoTReasoner(llm=self.llm)
        
        # Initialize the sensor data manager
        self.sensor_manager = SensorDataManager()
        
        # Initialize the output generator
        self.output_generator = OutputGenerator()
        
        # Internal state variables
        self.world_model = {}
        self.event_queue = []
        
        logger.info(f"SoTAgent initialized with model: {self.model_name}")
    
    def ingest_data(self, data: Optional[Dict[str, Any]] = None) -> List[str]:
        """
        Ingest and process data from sensors or external sources.
        
        Args:
            data: Optional external data to ingest
            
        Returns:
            List of detected events
        """
        # Get data from sensors if not provided externally
        if data is None:
            data = self.sensor_manager.read_all_sensors()
        
        # Process and update the world model
        processed_data = self.sensor_manager.preprocess_data(data)
        self.world_model.update(processed_data)
        
        # Detect events based on the updated world model
        events = self.sensor_manager.detect_events(self.world_model)
        if events:
            self.event_queue.extend(events)
            logger.debug(f"Detected events: {events}")
        
        return events
    
    def process(self, query: Optional[str] = None) -> Dict[str, Any]:
        """
        Process a query or an event using SoT reasoning.
        
        Args:
            query: Optional user query to process
            
        Returns:
            Response containing reasoning and output
        """
        # Determine what to process: query or next event
        task = query
        if task is None and self.event_queue:
            task = self.event_queue.pop(0)
        
        if task is None:
            logger.debug("No task to process")
            return {"status": "idle"}
        
        # Log the task being processed
        logger.info(f"Processing task: {task[:50]}..." if len(str(task)) > 50 else f"Processing task: {task}")
        
        # Use the SoT reasoner to process the task
        reasoning_result = self.reasoner.reason(
            task=task,
            world_model=self.world_model
        )
        
        # Generate appropriate output format
        output = self.output_generator.generate_output(reasoning_result)
        
        # Create the response
        response = {
            "status": "success",
            "input": task,
            "reasoning": reasoning_result,
            "output": output,
            "timestamp": time.time()
        }
        
        return response
    
    def act(self, response: Dict[str, Any]) -> Any:
        """
        Take action based on the reasoning response.
        
        Args:
            response: The reasoning response
            
        Returns:
            Result of the action
        """
        # Extract action from response if present
        if "action" in response.get("output", {}):
            action = response["output"]["action"]
            logger.info(f"Taking action: {action['type']}")
            
            # Implement different action types here
            # Example: control an actuator, send a notification, etc.
            return {"action_taken": action["type"], "status": "completed"}
        
        return {"status": "no_action_required"}
    
    def run_once(self, query: Optional[str] = None) -> Dict[str, Any]:
        """
        Run one complete cycle of the agent: ingest, process, act.
        
        Args:
            query: Optional user query to process
            
        Returns:
            Result of the cycle
        """
        # Ingest data
        events = self.ingest_data()
        
        # Process the query or event
        response = self.process(query)
        
        # Take action if needed
        action_result = self.act(response)
        
        # Combine results
        result = {
            **response,
            "action_result": action_result,
            "events_detected": events
        }
        
        return result
    
    def run_interactive(self):
        """
        Run the agent in interactive mode, accepting user queries.
        """
        print("Sketch-of-Thought AI Agent - Interactive Mode")
        print("Type 'exit' to quit.")
        
        while True:
            try:
                query = input("\n> ")
                if query.lower() in ["exit", "quit"]:
                    break
                
                # Run the agent cycle
                result = self.run_once(query)
                
                # Display the output
                if "output" in result and "text" in result["output"]:
                    print(f"\nAgent: {result['output']['text']}")
                    
                    # Display any visualizations
                    if "visualization" in result["output"]:
                        vis_type = result["output"]["visualization"]["type"]
                        print(f"\n[{vis_type} visualization available]")
                else:
                    print(f"\nAgent: {result}")
            
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                logger.error(f"Error in interactive mode: {str(e)}")
                print(f"Error: {str(e)}")
    
    def run_server(self):
        """
        Run the agent in server mode, responding to API requests.
        """
        # Placeholder for server implementation
        # This would typically involve setting up an API server
        # using FastAPI, Flask, etc.
        logger.info("Server mode not implemented yet")
        print("Server mode not implemented yet")
    
    def run_demo(self):
        """
        Run a demonstration of the agent's capabilities.
        """
        # Execute a sequence of demo queries
        demo_queries = [
            "What is the current temperature?",
            "Analyze the trend of humidity over the last hour",
            "Is there any unusual activity detected in the environment?"
        ]
        
        print("Sketch-of-Thought AI Agent - Demo Mode\n")
        
        # Simulate sensor data for demo
        demo_data = {
            "temperature": 22.5,  # Celsius
            "humidity": 45.2,    # Percent
            "motion": False,     # No motion detected
            "time": time.time()
        }
        
        # Update the world model with demo data
        self.ingest_data(demo_data)
        
        # Process each demo query
        for query in demo_queries:
            print(f"\nQuery: {query}")
            result = self.run_once(query)
            
            if "output" in result and "text" in result["output"]:
                print(f"Agent: {result['output']['text']}")
                
                # Display reasoning sketch if available
                if "reasoning_sketch" in result:
                    print(f"\nReasoning Sketch:\n{result['reasoning_sketch']}")
            else:
                print(f"Agent: {result}")
            
            time.sleep(1)  # Pause between demo queries
