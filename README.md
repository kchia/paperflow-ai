# PaperFlow AI - Multi-Agent Business Automation System

An intelligent multi-agent system designed to automate core business operations for a paper manufacturing company. This system demonstrates advanced agent orchestration, natural language processing, and enterprise workflow automation.

## Overview

PaperFlow AI is a production-ready multi-agent system that automates critical business processes including inventory management, dynamic quote generation, and order fulfillment. Built with modern Python agent frameworks and LLM integration, the system handles complex workflows through coordinated agent communication and data-driven decision making.

### Key Capabilities

- **Intelligent Inventory Management**: Real-time stock monitoring and automated restocking decisions
- **Dynamic Quote Generation**: Context-aware pricing with historical data analysis and bulk discount calculations
- **Automated Order Fulfillment**: End-to-end transaction processing with supplier coordination
- **Text-based Agent Communication**: Fully automated workflow orchestration using natural language

### Technical Stack

- **Agent Frameworks**: smolagents, pydantic-ai, or npcsh for orchestration
- **Data Processing**: sqlite3, pandas for business intelligence
- **LLM Integration**: OpenAI-compatible API for natural language understanding
- **Architecture**: Multi-agent system with up to 5 specialized agents

---

## Project Structure

- `project_starter.py`: Core implementation of the multi-agent orchestration system
- `quotes.csv`: Historical quote database for pricing intelligence
- `quote_requests.csv`: Customer request processing pipeline
- `quote_requests_sample.csv`: Test scenarios and validation suite

---

## Setup

### Prerequisites

- Python 3.8+
- OpenAI-compatible API key

### Installation

1. **Install dependencies**

```bash
pip install -r requirements.txt
```

2. **Install agent framework** (choose one)

```bash
# Option 1: smolagents
pip install smolagents

# Option 2: pydantic-ai
pip install pydantic-ai

# Option 3: npcsh
pip install npcsh[lite]
```

3. **Configure environment**

Create a `.env` file with your API credentials:

```
UDACITY_OPENAI_API_KEY=your_api_key_here
```

## Usage

Run the system with the test scenarios:

```bash
python project_starter.py
```

The system will:
1. Process customer requests through the multi-agent pipeline
2. Coordinate inventory checks, quote generation, and order fulfillment
3. Execute transactions and update financial records
4. Generate comprehensive reports and logs

### Output

- Real-time agent communication logs
- Inventory and cash flow updates
- Financial reports
- `test_results.csv`: Complete interaction history and audit trail

## System Architecture

The multi-agent system uses a coordinated workflow where specialized agents handle distinct business functions. Agent communication follows a text-based protocol, enabling flexible orchestration and natural language processing throughout the pipeline.

For detailed architecture diagrams and design documentation, see the workflow diagrams included in this repository.

## Features

- **Historical Data Integration**: Leverages past quotes for intelligent pricing
- **Bulk Discount Logic**: Automatic discount calculations based on order volume
- **Database-Driven Operations**: SQLite backend for reliable data persistence
- **Comprehensive Logging**: Full audit trails for compliance and debugging
- **Modular Agent Design**: Extensible architecture for future capabilities

---