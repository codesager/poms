"""
P.O.T.S - Portfolio, OMS and Transactions System
Pydantic models and LangChain setup for portfolio management
"""
import os
import datetime
import uuid
from typing import List, Optional, Dict, TypedDict

from pydantic import BaseModel, Field, model_validator
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from langchain_openai import ChatOpenAI
from dotenv import find_dotenv, load_dotenv

# Load environment variables
load_dotenv(find_dotenv())
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize LLM
llm = ChatOpenAI(api_key=OPENAI_API_KEY)

# Pydantic Models
class PortfolioHolding(BaseModel):
    ticker: Optional[str] = Field(default=None, description="ticker or list of tickers to fetch holdings for")
    accounts: Optional[List[str]] = Field(default=None, description="list of accounts to view holdings for")
    start_date: Optional[str] = Field(default=None, description="start date to evaluate the performace of accounts, if nothing is provided, consider it as today")
    end_date: Optional[str] = Field(default=None, description="end date to evaluate the performance of accounts")
    fields: Optional[List[str]] = Field(default=None, description="list of fields to fetch data for. These can be exposure, yield, duration, market value, price")

    @model_validator(mode='before')
    def process_dates(cls, values):
        if isinstance(values, dict):
            start_date = values.get('start_date')
            end_date = values.get('end_date')
            
            if start_date == None:
                values['start_date'] = datetime.date.today().isoformat()

            if start_date == 'today':
                values['start_date'] = datetime.date.today().isoformat()
            if end_date == 'today':
                values['end_date'] = datetime.date.today().isoformat()
                
            if start_date == 'YTD':
                values['start_date'] = f'{datetime.date.today().year}-01-01'
                values['end_date'] = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
        return values

class PortfolioPerformance(BaseModel):
    start_date: Optional[str] = Field(default=None, description="start date to evaluate the performace of accounts")
    end_date: Optional[str] = Field(default=None, description="end date to evaluate the performance of accounts")
    accounts: Optional[str] = Field(default=None, description="a single account or list of accounts to view performance")
    
    @model_validator(mode='before')
    def process_dates(cls, values):
        if isinstance(values, dict):
            start_date = values.get('start_date')
            end_date = values.get('end_date')
            
            if start_date == None:
                values['start_date'] = datetime.date.today().isoformat()

            if start_date == 'today':
                values['start_date'] = datetime.date.today().isoformat()
            if end_date == 'today':
                values['end_date'] = datetime.date.today().isoformat()
                
            if start_date == 'YTD':
                values['start_date'] = f'{datetime.date.today().year}-01-01'
                values['end_date'] = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
        return values

class Order(BaseModel):
    """Information about a trading order."""
    action: Optional[str] = Field(default=None, description="buy, sell or hold")
    ticker: Optional[str] = Field(default=None, description="ticker you want to trade")
    quantity: Optional[int] = Field(default=None, description="number of units to be traded")
    weight: Optional[float] = Field(default=None, description="weight of the total portfolio, usually in percentages")
    accounts: Optional[List[str]] = Field(default=None, description="a list of accounts to buy or sell orders")

# Collection models
class Orders(BaseModel):
    """Extracted data about orders."""
    orders: List[Order]

class Holdings(BaseModel):
    """Extracted data about holdings."""
    holdings: List[PortfolioHolding]

class Performances(BaseModel):
    """Extracted data about performance."""
    performances: List[PortfolioPerformance]

# Example handling
class Example(TypedDict):
    """A representation of an example consisting of text input and expected tool calls."""
    input: str
    tool_calls: List[BaseModel]

def tool_example_to_messages(example: Example) -> List[BaseMessage]:
    """Convert an example into a list of messages that can be fed into an LLM."""
    messages: List[BaseMessage] = [HumanMessage(content=example["input"])]
    openai_tool_calls = []
    for tool_call in example["tool_calls"]:
        openai_tool_calls.append(
            {
                "id": str(uuid.uuid4()),
                "type": "function",
                "function": {
                    "name": tool_call.__class__.__name__,
                    "arguments": tool_call.model_dump_json(),
                },
            }
        )
    messages.append(
        AIMessage(content="", additional_kwargs={"tool_calls": openai_tool_calls})
    )
    tool_outputs = example.get("tool_outputs") or [
        "You have correctly called this tool."
    ] * len(openai_tool_calls)
    for output, tool_call in zip(tool_outputs, openai_tool_calls):
        messages.append(ToolMessage(content=output, tool_call_id=tool_call["id"]))
    return messages

# Create examples
order_examples = [
    (
        "Buy 250 AAPL in account capers",
        Order(action="buy", quantity=250, ticker="aapl", accounts=["capers"]),
    ),
    (
        "Sell 500 TSLA in accounts capers, ushy and halifax",
        Order(action="sell", ticker="tsla", quantity=500, accounts=["capers", "ushy", "halifax"]),
    ),
    (
        "Roll 500 MSFT",
        Order(action="roll", ticker="msft", quantity=500, accounts=None),
    ),
    (
        "Increase exposure to aapl by 0.5%",
        Order(action="buy", ticker="aapl", quantity=None, weight=0.5, accounts=None)
    ),
    (
        "Decrease exposure to aapl by 0.5%",
        Order(action="sell", ticker="aapl", quantity=None, weight=0.5, accounts=None)
    )
]

portfolio_holdings_examples = [
    (
        "what are my holdings in account ABC as of today",
        PortfolioHolding(ticker=None, accounts=['ABC'], start_date='today', end_date=None, fields=['weight', 'price', 'mv', 'yield']),
    ),
    (
        "show me positions of TSLA in my account CAPERS",
        PortfolioHolding(ticker='TSLA', accounts=['CAPERS'], start_date='today', end_date=None, fields=['weight', 'price', 'mv', 'yield']),
    ),
    (
        "what's my exposure to MSFT in my accounts HALIFAX, MANIFAX and SIMFAX as of 31-Dec-2023",
        PortfolioHolding(ticker='MSFT', accounts=['HALIFAX', 'MANIFAX', 'SIMFAX'], start_date='31-Dec-2023', end_date=None, fields=['weight', 'price', 'mv', 'yield']),
    ),
    (
        "Show change of my positions in all of my accounts between 01-Jan-2024 to 31-Mar-2024",
        PortfolioHolding(ticker=None, accounts=['ALL'], start_date='01-Jan-2024', end_date='31-Mar-2024', fields=['weight', 'price', 'mv', 'yield']),
    )
]

portfolio_performance_examples = [
    (
        "what are my returns in account capers, ushy",
        PortfolioPerformance(accounts='capers,ushy', start_date='05-May-2024', end_date='02-May-2024'),
    )
]

# Convert examples to messages
order_messages = []
holding_messages = []
performance_messages = []

for text, tool_call in order_examples:
    order_messages.extend(
        tool_example_to_messages({"input": text, "tool_calls": [tool_call]})
    )
    
for text, tool_call in portfolio_holdings_examples:
    holding_messages.extend(
        tool_example_to_messages({"input": text, "tool_calls": [tool_call]})
    )

for text, tool_call in portfolio_performance_examples:
    performance_messages.extend(
        tool_example_to_messages({"input": text, "tool_calls": [tool_call]})
    )

# Create prompts
holding_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert extraction algorithm. "
        "Only extract relevant information from the text. "
        "When user inputs today, convert it to system date "
        "Extract portfolio holdings information from the given text "
        "If you do not know the value of an attribute asked to extract, "
        "return null for the attribute's value.",
    ),
    MessagesPlaceholder('portfolio_holdings_examples'),
    ("human", "{text}"),
])

order_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert extraction algorithm. "
        "Only extract relevant information from the text. "
        "Extract order details information from the given text "
        "If you do not know the value of an attribute asked to extract, "
        "return null for the attribute's value.",
    ),
    MessagesPlaceholder('order_examples'),
    ("human", "{text}"),
])

performance_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert extraction algorithm. "
        "Only extract relevant information from the text. "
        "Extract portfolio performance information from the given text "
        "If you do not know the value of an attribute asked to extract, "
        "return null for the attribute's value.",
    ),
    MessagesPlaceholder('portfolio_performance_examples'),
    ("human", "{text}"),
])

# Create runnables
order_runnable = order_prompt | llm.with_structured_output(
    schema=Orders,
    method='function_calling',
    include_raw=False
)

portfolio_holding_runnable = holding_prompt | llm.with_structured_output(
    schema=Holdings,
    method='function_calling',
    include_raw=False
)

portfolio_performance_runnable = performance_prompt | llm.with_structured_output(
    schema=Performances,
    method='function_calling',
    include_raw=False
)

def route_input_and_extract(text):
    """Route input text to appropriate extraction pipeline."""
    if "buy" in text.lower() or "sell" in text.lower() or ("increase" in text.lower() or "decrease" in text.lower()):
        return order_runnable.invoke({"order_examples": [], "text": text})
    elif any(keyword in text.lower() for keyword in ["hold", "position", "exposure", "yield", "duration"]):
        return portfolio_holding_runnable.invoke({"portfolio_holdings_examples": [], "text": text})
    elif any(keyword in text.lower() for keyword in ["performance", "return"]):
        return portfolio_performance_runnable.invoke({"portfolio_performance_examples": [], "text": text})
    else:
        return None
