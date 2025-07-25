# LLM Experiments

Repository for running various experiments with Large Language Models (LLMs) and exploring different GenAI frameworks and approaches.

## Experiments

### Deep Research Assistant
- Multi-round research generation using LangGraph orchestration
- Topic-based Q&A with validation and summarization
- Examples: NFL GOAT analysis, Bitcoin investment research, Tesla purchase decision making

<div align="center">
  <img src="output/research_experiment/langgraph.png" alt="Research Experiment Graph" width="350">
</div>

### Social Media Agentic Team
- Experiment with an agentic team of social media agents. Given a topic / social media post idea, multiple agents will kick off to generate content for specific social media platforms.

<div align="center">
  <h4>Agentic Flow (Platform-agnostic)</h4>
  <img src="output/social_media_experiment/langgraph_subgraph.png" alt="Social Media Agentic Team Graph" width="250">
</div>

### Ambient Agent
- Experiment with an ambient agent that can be used to interact with the user in a chat-like manner.
  - Slack integration for human-in-the-loop ([Jupyter Notebook](nb/ambient_experiment/test_tools.ipynb))
    - Handles images, text, and basic file uploads
  - 'Real' stock data generation and saving plots to folder for later multi-modal LLM analysis
  
  
### Flight Data Analysis

- Experiment with flight data retrieval and analysis using custom flight search tools
- AI-powered flight assistant with OpenAI's tool calling capabilities
  - Custom flight search tools with real-time data retrieval and processing
  - Integrated memory and conversation history management
  - Streaming responses with real-time tool execution events
  - Interactive console-based conversation interface
    - `fast-flights` does not work from terminal due to playwright issues, but from notebook demo is smooth
- Comparison between tool-calling agent and manual price optimization
  - Fetching flight information for multiple destinations
  - Dynamic visualization of price distributions
  - Detailed flight data analysis including prices, durations, and options
- [Jupyter Notebook](nb/flights/flights.ipynb)

### Deep Research with o3 + gpt-4.1
- This experiment tests deep research capabilities by employing a two-agent setup using the Agents SDK. 
- A primary research agent, powered by 'o3', orchestrates a 'gpt-4.1'-powered web search agent.
- The primary agent breaks down a complex research query, delegates web searches, and synthesizes the gathered information into a comprehensive report. 
- Code Interpreter tool test
- [Jupyter Notebook](nb/deep_research_o3_gpt41.ipynb)

<div align="center">
  <h4>Agent with tools (OpenAI Agents SDK)</h4>
  <img src="output/agents_sdk_experiments/web_search_agent_graph.png" alt="o3 with tools" width="400">
</div>

<div align="center">
  <h4>Agent with tools (OpenAI Agents SDK)</h4>
  <img src="output/agents_sdk_experiments/deep_research_agent_graph.png" alt="o3 with tools" width="300">
</div>

*More experiments to be added...*

## Tests

### Anthropic Citations

- Testing new `citations` feature in Anthropic
- Providing plain txt files, PDFs for 'RAG'-like tasks, such as QA and summarization - checking reference capabilities of `claude-3-5-sonnet-20241022`
- [Jupyter Notebook](nb/anthropic-citations.ipynb)

### OpenAI Response API and Agents Framework

- Response API
  - [Jupyter Notebook](nb/openai-response-api-experiments.ipynb)
  - structured output (json_schema)
  - web search tool
    - compare `gpt-4o-search-preview` model with `gpt-4o` + web search tool in Response API
    - multiple tools at once
  - file search tool
    - explore direct vector search (manual RAG) vs. file search tool
    - custom chunking and retrieval settings
  - Computer Use tool
    - Installed playwright browser to use it as a tool in the agentic loop
    - Due to Zero Data Retention policy of OpenAI, the tool is not yet available for me for testing
    - In a browser, a screenshot is taken to decide on the next action
  - Conversation State
    - `previous_response_id` is used to handle the conversation history if org does not have Zero Data Retention policy

- Agents Framework

  - [Jupyter Notebook](nb/openai-agents-framework-experiments.ipynb)
  - Agents and their powerful arguments (instructions, handoffs, tools, etc.)
  - Tools (built in such as WebSearch, custom, agents-as-tools)
    - native tool calling and execution - no more manual function calling
  - Handoffs (passing the conversation to another agent)
    - Prompt prefixes to help LLMs understand handoffs
    - Handoff filters to limit the amount of information being sent to the next agent
  - Overall takeaways
    - Agent and tool calling is great, works usually as expected!
    - Handoffs are exremely prompt-sensitive
    - Handoffs many times dont actually happen, unless prompted strictly
    - For workflows, deterministic jobs such as LangGraph are much better. For open-ended tasks, where many many directions can be taken, handoffs might be a good option to run simulations.
    - `gpt-4.5-preview` is SO much better than `gpt-4o` for handoffs!

*More tests to be added...*

## Tech Stack

### Frameworks & Libraries
- OpenAI SDK
- Anthropic SDK
- LangGraph
- LangChain
- openai-agents-framework
- Perplexity AI


## Setup

1. Create virtual environment
2. Install requirements: `pip install -r requirements.txt`
3. Create `.env` file with required API keys

For `playwright` to work, you need to:
1. pip install pytest-playwright
2. playwright install

## Notes

This is a personal experimental repository for testing and learning about different LLM implementations and approaches. Experiments are typically contained in Jupyter notebooks for easy iteration and visualization. 