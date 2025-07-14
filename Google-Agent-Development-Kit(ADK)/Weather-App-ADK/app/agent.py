# 1. Basic Agent
from google.adk.agents import Agent

basic_agent = Agent(
    model='gemini-2.0-flash-001',
    name='root_agent',
    description='A helpful assistant.',
    instruction='Give Answer to the user query',
)

# 2. Basic Agent with Tool
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

# 3. Agent with State
from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext
import yfinance as yf

def get_stock_price(ticker: str, tool_context: ToolContext):
    try:
        stock = yf.Ticker(ticker)
        price = stock.info.get('regularMarketPrice')
        
        #initialize recent searches if it doesn't exist
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

# 4. Multi Tool Agent
from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext
import yfinance as yf

def get_stock_price(ticker: str, tool_context: ToolContext):
    try:
        stock = yf.Ticker(ticker)
        price = stock.info.get('regularMarketPrice')
        
        #initialize recent searches if it doesn't exist
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
        

# 5. Structured Output Agent
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


root_agent= structured_agent