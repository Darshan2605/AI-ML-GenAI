# Building Real AI Agents with Google ADK: Features, Use Cases, and Hands-On Examples

## What is Google ADK?

Google’s Agent Development Kit (ADK) is an open-source Python framework for building, orchestrating, and deploying AI agents. Unlike simple chatbots, ADK lets you create teams of agents that can collaborate, use tools, and solve real problems—making your AI apps much more powerful and flexible.

---

## Why Use Google ADK?

- **Build smart assistants:** Go beyond chatbots—create agents that can answer questions, fetch data, make decisions, and even use other agents as helpers.
- **Automate workflows:** Orchestrate multi-step processes, like generating reports, summarizing documents, or managing tasks.
- **Integrate with APIs and tools:** Agents can call external APIs, use Python functions, or even interact with databases and cloud services.
- **Create multi-agent systems:** Design teams of agents that work together, each specializing in different tasks.

---

## Key Features

- **Modular agent types:** Choose from LLM agents, workflow agents, or custom logic agents.
- **Tooling support:** Easily add tools (functions, APIs) that agents can use to fetch data or perform actions.
- **Multi-agent orchestration:** Build systems where agents can call each other, delegate tasks, and coordinate.
- **Streaming and UI:** Debug and watch your agents work in real time with a built-in web UI.
- **Model-agnostic:** Use Gemini, Claude, Mistral, or other LLMs—you're not locked into one provider.
- **Flexible deployment:** Run agents locally, in Docker, on Google Cloud Run, or anywhere Python runs.

---

## Alternatives

- **LangChain:** Popular for chaining LLM calls and tools, but less focused on multi-agent orchestration.
- **Microsoft AutoGen:** Another open-source framework for building multi-agent LLM systems.
- **CrewAI:** Focuses on collaborative agent teams, similar to ADK.
- **OpenAI Function Calling:** Lets you add tool use to OpenAI models, but doesn't provide full agent orchestration.

---

## Real-World Use Cases

- **Business automation:** Agents that generate proposals, summarize documents, or manage customer support tickets.
- **Finance:** Stock advisors that fetch prices, analyze trends, and give recommendations.
- **Social media:** Content creation pipelines where agents find trends, write posts, and suggest visuals.
- **Research assistants:** Agents that search the web, summarize findings, and organize information.
- **Home automation:** Agents that control smart devices, schedule routines, and respond to voice commands.
- **Education:** Tutors that answer questions, grade assignments, and provide feedback.

---

## In Simple Terms

Google ADK helps you build real AI assistants—not just chatbots. You can give your agents tools, let them work together, and deploy them anywhere. It's like having a team of smart helpers, each with their own skills, working together to get things done.

---

# Hands-On: Building Agents with Google ADK

## Project Overview

This project demonstrates the use of Google ADK to build intelligent agents capable of answering user queries, fetching real-time stock prices, providing company information, and giving structured stock recommendations. The app showcases various agent patterns, including basic agents, tool-augmented agents, stateful agents, multi-tool agents, and agents with structured output.

---

## Key Components

- **Basic Agent:** Answers general user queries using a language model.
- **Tool Agent:** Integrates external tools (e.g., yfinance) to fetch real-time stock prices.
- **Stateful Agent:** Remembers user context, such as recent stock searches, across interactions.
- **Multi-Tool Agent:** Handles multiple types of queries (e.g., price and company info) using different tools.
- **Structured Output Agent:** Returns recommendations in a strict JSON format for easy integration and validation.
- **Extensible Design:** Easily add new tools or agent types as needed.

---

## Installation

```bash
pip install google-adk yfinance pydantic
```

---

## Creating a Basic Agent

```python
from google.adk.agents import Agent

root_agent = Agent(
    model='gemini-2.0-flash-001',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
)
```

---

## Adding a Tool: Fetching Stock Prices

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
```

---

## Stateful Agent: Remembering Recent Searches

```python
from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext
import yfinance as yf

def get_stock_price(ticker: str, tool_context: ToolContext):
    try:
        stock = yf.Ticker(ticker)
        price = stock.info.get('regularMarketPrice')
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
```

---

## Multi-Tool Agent: Price and Company Info

```python
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

---

## Structured Output Agent: JSON Recommendations

```python
from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field

class StockAnalysis(BaseModel):
    ticker: str = Field(description="Stock symbol")
    recommendation: str = Field(description="Buy or Sell recommendation")

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

---

## Running Your Agent

- **Terminal:**  
  ```bash
  adk run app
  ```
- **Web Interface:**  
  ```bash
  adk web
  ```

---

## Final Thoughts

Google ADK is a powerful toolkit for building real AI agents that can do much more than chat. With modular design, tool integration, and multi-agent orchestration, you can build assistants that actually get things done. Whether you’re automating business processes, analyzing stocks, or building smart home assistants, ADK gives you the flexibility and power to bring your ideas to life.

---

*If you found this helpful, follow for more AI and agent development tutorials!* 