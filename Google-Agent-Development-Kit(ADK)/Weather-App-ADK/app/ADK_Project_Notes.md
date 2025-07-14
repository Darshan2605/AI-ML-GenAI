## Google ADK: Uses, Features, Alternatives, and Real-World Use Cases

### What is Google ADK?
Google's Agent Development Kit (ADK) is an open-source Python framework for building, orchestrating, and deploying AI agents. Unlike simple chatbots, ADK lets you create teams of agents that can collaborate, use tools, and solve real problems—making your AI apps much more powerful and flexible.

### Main Uses
- **Build smart assistants:** Go beyond chatbots—create agents that can answer questions, fetch data, make decisions, and even use other agents as helpers.
- **Automate workflows:** Orchestrate multi-step processes, like generating reports, summarizing documents, or managing tasks.
- **Integrate with APIs and tools:** Agents can call external APIs, use Python functions, or even interact with databases and cloud services.
- **Create multi-agent systems:** Design teams of agents that work together, each specializing in different tasks.

### Key Features
- **Modular agent types:** Choose from LLM agents, workflow agents, or custom logic agents.
- **Tooling support:** Easily add tools (functions, APIs) that agents can use to fetch data or perform actions.
- **Multi-agent orchestration:** Build systems where agents can call each other, delegate tasks, and coordinate.
- **Streaming and UI:** Debug and watch your agents work in real time with a built-in web UI.
- **Model-agnostic:** Use Gemini, Claude, Mistral, or other LLMs—you're not locked into one provider.
- **Flexible deployment:** Run agents locally, in Docker, on Google Cloud Run, or anywhere Python runs.

### Alternatives
- **LangChain:** Popular for chaining LLM calls and tools, but less focused on multi-agent orchestration.
- **Microsoft AutoGen:** Another open-source framework for building multi-agent LLM systems.
- **CrewAI:** Focuses on collaborative agent teams, similar to ADK.
- **OpenAI Function Calling:** Lets you add tool use to OpenAI models, but doesn't provide full agent orchestration.

### Real-World Use Cases
- **Business automation:** Agents that generate proposals, summarize documents, or manage customer support tickets.
- **Finance:** Stock advisors that fetch prices, analyze trends, and give recommendations.
- **Social media:** Content creation pipelines where agents find trends, write posts, and suggest visuals.
- **Research assistants:** Agents that search the web, summarize findings, and organize information.
- **Home automation:** Agents that control smart devices, schedule routines, and respond to voice commands.
- **Education:** Tutors that answer questions, grade assignments, and provide feedback.

### In Simple Terms
Google ADK helps you build real AI assistants—not just chatbots. You can give your agents tools, let them work together, and deploy them anywhere. It's like having a team of smart helpers, each with their own skills, working together to get things done.

---

## Project Overview

This project demonstrates the use of Google's Agent Development Kit (ADK) to build intelligent agents capable of answering user queries, fetching real-time stock prices, providing company information, and giving structured stock recommendations. The app showcases various agent patterns, including basic agents, tool-augmented agents, stateful agents, multi-tool agents, and agents with structured output.

---

## Key Features / Components

- **Basic Agent:** Answers general user queries using a language model.
- **Tool Agent:** Integrates external tools (e.g., yfinance) to fetch real-time stock prices.
- **Stateful Agent:** Remembers user context, such as recent stock searches, across interactions.
- **Multi-Tool Agent:** Handles multiple types of queries (e.g., price and company info) using different tools.
- **Structured Output Agent:** Returns recommendations in a strict JSON format for easy integration and validation.
- **Extensible Design:** Easily add new tools or agent types as needed.

---

## Installation Commands & Explanations

### 1. Google ADK Installation

**Command:**
```bash
pip install google-adk
```
**Explanation:**
- Installs the Google Agent Development Kit (ADK) Python package, which provides tools and APIs for building with Google’s AI models and agent development workflows.
- Uses `pip`, the Python package installer, to fetch and install the package from the Python Package Index (PyPI).

### 2. yfinance Installation

**Command:**
```bash
pip install yfinance
```
**Explanation:**
- Installs the `yfinance` Python library, which allows you to download historical market data from Yahoo Finance.
- Enables programmatic access to stock prices, financials, and other market data for use in your projects.

---

## Creating a Google ADK App

### What is a Basic Agent in Google's ADK?
A **basic agent** in Google's Agent Development Kit (ADK) is a minimal implementation of an agent that can process user instructions using a language model. It is typically defined in a Python file (e.g., `agent.py`) with a variable named `root_agent`:

```python
from google.adk.agents import Agent

root_agent = Agent(
    model='gemini-2.0-flash-001',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
)
```

### How to Create an ADK App
1. **Create a directory for your agent** (e.g., `app/`).
2. **Inside that directory, add:**
   - `agent.py` (with the `root_agent` definition as above)
   - `__init__.py` (can be empty or import agent)
   - `requirements.txt` (list your dependencies, e.g., `google-adk`)
3. **(Optional)** Add a `.env` file for environment variables (API keys, etc.).

### How to Run the App Using the ADK Command
- Make sure you have the ADK CLI installed:
  ```bash
  pip install google-adk
  ```
- From your project root, run:
  ```bash
  adk run app
  ```
- With Web Interface, run:
  ```bash
  adk web
  ```
  Replace `app` with your agent directory name if different.
- This will start your agent locally, allowing you to interact with it via the terminal or web UI (if enabled).


---

## Basic Agent with Tool Example

### Code Example
```python
from google.adk.agents import Agent
import yfinance as yf

def get_stock_price(ticker: str):
    try:
        stock = yf.Ticker(ticker)
        price = stock.info.get('regularMarketPrice')
        if price is not None:
            return f"The current price of {ticker.upper()} is {price} USD."
        else:
            return f"Could not retrieve the price for {ticker.upper()}."
    except Exception as e:
        return f"Error fetching stock price: {str(e)}"

tool_agent = Agent(
    model='gemini-2.0-flash-001',
    name='tool_agent',
    description='An agent that provides current stock prices using yfinance.',
    instruction='Answer user questions about stock prices using the get_stock_price tool.',
    tools=[get_stock_price]
)

root_agent = tool_agent
```

### Explanation
- **Purpose:** This agent is enhanced with a tool function (`get_stock_price`) that allows it to fetch real-time stock prices using the `yfinance` library.
- **How it works:**
  - The `get_stock_price` function takes a stock ticker symbol (e.g., "AAPL") and returns the current market price using Yahoo Finance data.
  - The `tool_agent` is an ADK agent configured to use this tool. When a user asks about a stock price, the agent can call the tool to fetch and return the latest price.
- **Why use tools:** Tools extend the agent's capabilities beyond language understanding, allowing it to perform real-world actions like fetching data, calling APIs, or running calculations.
- **Usage:** With this setup, you can ask your agent questions like "What is the price of TSLA?" and it will respond with the latest price using the tool.

---

## Stateful Agent Example

### Code Example
```python
from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext
import yfinance as yf

def get_stock_price(ticker: str, tool_context: ToolContext):
    try:
        stock = yf.Ticker(ticker)
        price = stock.info.get('regularMarketPrice')
        # Initialize recent searches if it doesn't exist
        if "recent_searches" not in tool_context.state:
            tool_context.state["recent_searches"] = []
        recent_searches = tool_context.state["recent_searches"]
        if ticker not in recent_searches:
            recent_searches.append(ticker)
            tool_context.state["recent_searches"] = recent_searches
        if price is not None:
            return f"The current price of {ticker.upper()} is {price} USD."
        else:
            return f"Could not retrieve the price for {ticker.upper()}."
    except Exception as e:
        return f"Error fetching stock price: {str(e)}"

stateful_agent = Agent(
    model='gemini-2.0-flash-001',
    name='stateful_agent',
    description='An agent that provides current stock prices using yfinance.',
    instruction='Answer user questions about stock prices using the get_stock_price tool.',
    tools=[get_stock_price]
)

root_agent = stateful_agent
```

### Explanation
- **Purpose:** This agent not only fetches the current stock price using the `yfinance` library, but also keeps track of the user's recent stock ticker searches using the agent's state.
- **How it works:**
  - The `get_stock_price` function takes a stock ticker and a `ToolContext` object (provided by ADK).
  - It fetches the current price for the ticker using yfinance.
  - It checks if the `recent_searches` list exists in the agent's state; if not, it initializes it.
  - If the ticker is not already in `recent_searches`, it adds it, allowing the agent to remember which tickers the user has asked about previously.
  - Returns a message with the current price or an error message if something goes wrong.
- **Stateful Tools:** By using `ToolContext`, the tool can read and write to the agent's state, enabling more advanced, context-aware behaviors.
- **Usage:** This setup allows the agent to provide not just answers, but also context-aware responses or features (like showing a history of recent searches).

---

## Multi-Tool Agent Example

### Code Example
```python
from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext
import yfinance as yf

def get_stock_price(ticker: str, tool_context: ToolContext):
    try:
        stock = yf.Ticker(ticker)
        price = stock.info.get('regularMarketPrice')
        # Initialize recent searches if it doesn't exist
        if "recent_searches" not in tool_context.state:
            tool_context.state["recent_searches"] = []
        recent_searches = tool_context.state["recent_searches"]
        if ticker not in recent_searches:
            recent_searches.append(ticker)
            tool_context.state["recent_searches"] = recent_searches
        if price is not None:
            return f"The current price of {ticker.upper()} is {price} USD."
        else:
            return f"Could not retrieve the price for {ticker.upper()}."
    except Exception as e:
        return f"Error fetching stock price: {str(e)}"

def get_stock_info(ticker: str):
    try:
        stock = yf.Ticker(ticker)
        company_name = stock.info.get('longName')
        sector = stock.info.get('sector')
        industry = stock.info.get('industry')
        if company_name:
            return f"The company name for {ticker.upper()} is {company_name}. The sector is {sector} and the industry is {industry}."
        else:
            return f"Could not retrieve the company name for {ticker.upper()}."
    except Exception as e:
        return f"Error fetching stock info: {str(e)}"

multi_tool_agent = Agent(
    model='gemini-2.0-flash-001',
    name='multi_tool_agent',
    description='An agent that provides current stock prices and info using yfinance.',
    instruction='Answer user questions about stock prices and info using the get_stock_price and get_stock_info tools.',
    tools=[get_stock_price, get_stock_info]
)
```

### Explanation
- **Purpose:** This agent is equipped with multiple tools, allowing it to provide both stock prices and detailed company information using the `yfinance` library.
- **How it works:**
  - **`get_stock_price`**: Fetches the current market price for a given stock ticker and tracks recent searches in the agent's state.
  - **`get_stock_info`**: Retrieves detailed company information including the company name, sector, and industry for a given stock ticker.
  - The agent can choose which tool to use based on the user's query, making it more versatile and capable of handling a wider range of questions.
- **Multi-Tool Capability:** By registering multiple tools with the agent, it can perform different types of tasks and provide more comprehensive responses to user queries.
- **Usage:** Users can ask questions like "What is the price of TSLA?" or "Tell me about the company TSLA" and the agent will use the appropriate tool to provide the relevant information.
- **State Management:** The `get_stock_price` tool maintains a list of recent searches, while `get_stock_info` is a stateless tool that provides company details.

---

## Structured Output Agent Example

### Code Example
```python
from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field
import yfinance as yf

class StockAnalysis(BaseModel):
    ticker: str = Field(description="Stock symbol")
    recommendation: str = Field(description="Buy or Sell recommendation")

# Define a function to get stock data for our prompt
def get_stock_data_for_prompt(ticker):
    stock = yf.Ticker(ticker)
    price = stock.info.get("currentPrice", 0)
    target_price = stock.info.get("targetMeanPrice", 0)
    return price, target_price

structured_agent = LlmAgent(
    name="structured_agent",
    model="gemini-2.0-flash",
    description="An agent with structured output",
    instruction="""
    You are a stock advisor. Analyze the stock ticker provided by the user.
    Return Buy or Sell recommendation in JSON format.
    
    For each ticker, look at the price and target price to make a decision.
    If target price > current price: recommend Buy
    Otherwise: recommend Sell
    """,
    output_schema=StockAnalysis,
    output_key="stock_analysis"
)
```

### Explanation
- **Purpose:** This agent provides structured, JSON-formatted stock recommendations (Buy or Sell) for a given ticker, using a Pydantic model to enforce the output structure.
- **How it works:**
  - The `StockAnalysis` Pydantic model defines the expected output: a `ticker` and a `recommendation` (Buy or Sell).
  - The agent is instructed to compare the current price and target price for the stock:
    - If the target price is higher than the current price, recommend "Buy".
    - Otherwise, recommend "Sell".
  - The output is always in JSON format matching the `StockAnalysis` schema.
- **Helper Function:** `get_stock_data_for_prompt` fetches the current and target prices for a given ticker using yfinance.
- **Why Structured Output?**
  - **Reliability:** Ensures the agent’s response always follows a predictable format.
  - **Integration:** Makes it easy to use the agent’s output in other systems or for further processing.
  - **Validation:** Pydantic automatically checks that the output matches the expected schema.
- **Example Output:**
  ```json
  {
    "ticker": "AAPL",
    "recommendation": "Buy"
  }
  ```

---


