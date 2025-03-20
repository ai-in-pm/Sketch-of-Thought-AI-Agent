# Sketch-of-Thought AI Agent

An AI agent with real-time environmental awareness that utilizes Sketch-of-Thought (SoT) reasoning for efficient decision-making. This project integrates instruction-following capabilities with SoT reasoning patterns to create an agent that can perceive, process, and act in real-time environments.

The development of this repository was inspired by the paper "Sketch-of-Thought: Efficient LLM Reasoning with Adaptive Cognitive-Inspired Sketching". To read the entire paper, visit https://arxiv.org/pdf/2503.05179

## Features

- **Real-Time Interaction**: Process streaming data from multiple sensors and data sources
- **Multimodal Perception**: Understand the physical world through vision, audio, and numeric inputs
- **Sketch-of-Thought Reasoning**: Efficient reasoning using concise thought patterns
- **Structured Outputs**: Generate graphs, diagrams, equations, and step-by-step explanations
- **Integration with LLMs**: Leverage models like GPT-4 for complex reasoning
- **Instruction Following**: Precise execution of structured instructions with verification
- **Visual Reasoning Sketches**: Generate visual representations of reasoning processes

## Installation

```bash
# Create and activate a virtual environment
python -m venv venv

# On Windows
.\venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
# Copy .env.example to .env and fill in your API keys
```

For detailed installation instructions, see [GETTING_STARTED.md](GETTING_STARTED.md).

## Project Structure

```
.
├── README.md                 # Project documentation
├── GETTING_STARTED.md        # Detailed setup instructions
├── LICENSE                   # MIT License
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables
├── src/                      # Source code
│   ├── agent/                # AI agent core components
│   │   ├── core.py           # Main agent logic
│   │   └── instruction_following.py # Instruction processing
│   ├── models/               # ML models and integrations
│   │   └── llm.py            # LLM interface
│   ├── reasoning/            # SoT reasoning implementations
│   │   └── sot.py            # Sketch-of-Thought paradigms
│   ├── sensors/              # Sensor data processing
│   │   └── data_manager.py   # Sensor data collection
│   ├── visualization/        # Output visualization tools
│   │   ├── outputs.py        # Output generation
│   │   └── sketch_renderer.py # Reasoning visualization
│   └── main.py               # Entry point
└── examples/                 # Example applications
    ├── sot_agent_demo.py     # Interactive demo
    ├── sketch_visualization_demo.py # Visualization examples
    ├── instruction_following_test.py # Instruction test
    ├── mock_reasoning_test.py # Mock reasoning test
    ├── instruction_mock_test.py # Instruction mock test
    ├── view_images.html      # HTML viewer for visualizations
    ├── view_test_results.html # Test results viewer
    └── view_instruction_test.html # Instruction test viewer
```

## Usage

```python
from src.agent.core import SoTAgent

# Initialize the agent
agent = SoTAgent()

# Process a query
result = agent.run_once("How does increased CO2 affect ocean acidity?")

# Access the output
print(result['output']['text'])

# Display reasoning sketch
print(result['output']['reasoning_sketch'])
```

## Running Examples

```bash
# Run the interactive demo
python examples/sot_agent_demo.py

# Run with specific mode
python examples/sot_agent_demo.py --mode demo
python examples/sot_agent_demo.py --mode instructions

# Run visualization demo
python examples/sketch_visualization_demo.py

# Run mock tests (no API key needed)
python examples/mock_reasoning_test.py
python examples/instruction_mock_test.py

# Start the HTML viewer server
cd examples
python -m http.server 8000
# Then open http://localhost:8000/view_test_results.html in your browser
```

## Sketch-of-Thought Reasoning Paradigms

The agent uses several reasoning paradigms to adapt to different tasks:

1. **Conceptual Chaining**: Connects concepts in a coherent chain of reasoning
   - Example: Tracing CO2 emissions → ocean acidification → marine ecosystem impacts
   - Visualization: Directed graph showing concept relationships

2. **Chunked Symbolism**: Breaks down complex problems into solvable symbolic chunks
   - Example: Mathematical calculations with step-by-step variable definitions
   - Visualization: Rendered equations with intermediate steps

3. **Expert Lexicon**: Applies domain-specific knowledge and terminology
   - Example: Medical diagnosis protocols or technical engineering solutions
   - Visualization: Structured hierarchical knowledge representation

## Visualization Capabilities

The agent can generate multiple visualization types:

- **Concept Chain Diagrams**: Visual representation of connected concepts
- **Equation Renderings**: Mathematical expressions with color-coded variables
- **Thought Trees**: Hierarchical representation of reasoning branches
- **Step-by-Step Explanations**: Annotated reasoning process
- **Data Graphs**: Visualization of numerical relationships

## Testing and Demo Tools

The project includes several tools for testing and demonstration:

- **Mock Reasoning Test**: Test the reasoning paradigms without API calls
- **Instruction Following Test**: Test the instruction processing capabilities
- **HTML Viewers**: Interactive web interfaces to view visualization outputs
- **Python API Examples**: Code snippets showing API usage patterns

## Environment Variables

Configure these in your `.env` file:

```
OPENAI_API_KEY=your_openai_api_key
MODEL_NAME=gpt-4
TEMPERATURE=0.7
DEBUG_MODE=False
LOG_LEVEL=info
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- The Sketch-of-Thought paradigm draws inspiration from various cognitive science theories
- Instruction following framework adapts concepts from instruction-following research
