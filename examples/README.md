# Sketch-of-Thought AI Agent Examples

This directory contains example scripts demonstrating the capabilities of the Sketch-of-Thought AI Agent.

## Available Examples

### SoT Agent Demo

A comprehensive demonstration of the agent's capabilities, including interactive mode, scripted demos, and instruction following.

```bash
# Run in interactive mode (default)
python sot_agent_demo.py

# Run a scripted demonstration
python sot_agent_demo.py --mode demo

# Run instruction following demonstration
python sot_agent_demo.py --mode instructions
```

## Creating Your Own Examples

You can create your own examples by importing the agent and its components:

```python
from src.agent.core import SoTAgent
from src.agent.instruction_following import InstructionProcessor, InstructionSet

# Initialize the agent
agent = SoTAgent()

# Run the agent with a query
result = agent.run_once("Your query here")

# Process the result
print(result['output']['text'])
```

## Notes

Ensure that you've set up your environment variables in the `.env` file before running the examples.
