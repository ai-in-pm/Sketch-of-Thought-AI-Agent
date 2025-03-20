# Getting Started with Sketch-of-Thought AI Agent

This guide will help you get started with the Sketch-of-Thought AI Agent, set up your environment, and run your first examples.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- OpenAI API key for LLM integration

## Installation

1. **Clone the repository**

```bash
git clone <repository-url>
cd Sketch-of-Thought\ AI\ Agent
```

2. **Create and activate a virtual environment**

```bash
# On Windows
python -m venv venv
.\venv\Scripts\activate

# On macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the root directory using the provided `.env.example` as a template:

```bash
cp .env.example .env
```

Then open the `.env` file and add your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key_here
MODEL_NAME=gpt-4
TEMPERATURE=0.7
DEBUG_MODE=False
LOG_LEVEL=info
```

## Running Examples

The project includes several example scripts to demonstrate different capabilities of the SoT AI Agent.

### Interactive Demo

Run the interactive demo to chat with the agent:

```bash
python examples/sot_agent_demo.py
```

### Scripted Demo

Run a demonstration of pre-defined queries:

```bash
python examples/sot_agent_demo.py --mode demo
```

### Instruction Following Demo

Run a demonstration of the instruction following capabilities:

```bash
python examples/sot_agent_demo.py --mode instructions
```

### Visualization Demo

Run a demonstration of the visualization capabilities:

```bash
python examples/sketch_visualization_demo.py
```

## Using the SoT AI Agent in Your Code

You can import and use the agent in your own code as follows:

```python
from src.agent.core import SoTAgent

# Initialize the agent
agent = SoTAgent()

# Process a query
result = agent.run_once("How does increased CO2 affect ocean acidity?")

# Access the output
print(result['output']['text'])

# Access the reasoning sketch
print(result['output']['reasoning_sketch'])
```

## Troubleshooting

### Missing Dependencies

If you encounter issues with missing dependencies, try installing them specifically:

```bash
pip install openai matplotlib networkx
```

### API Key Issues

If you receive authentication errors, ensure your OpenAI API key is correctly set in the `.env` file.

### Visualization Dependencies

For graph visualizations, you may need to install `pygraphviz` separately:

```bash
# On Windows (requires Visual C++ build tools)
pip install pygraphviz

# On macOS (requires Graphviz)
brew install graphviz
pip install pygraphviz

# On Linux
sudo apt-get install graphviz graphviz-dev
pip install pygraphviz
```

## Next Steps

- Explore the code in the `src` directory to understand the agent architecture
- Check out the different reasoning paradigms in `src/reasoning/sot.py`
- Extend the agent with new sensors or reasoning capabilities
- Create your own examples in the `examples` directory

## Getting Help

If you need assistance, please check the documentation or submit an issue on the repository.
