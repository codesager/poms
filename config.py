"""
Configuration settings for P.O.M.S - Portfolio and OMS System
"""
import streamlit as st

# Page configuration
PAGE_CONFIG = {
    "page_title": "P.O.M.S - Portfolio and OMS System",
    "page_icon": "📊",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Custom CSS styles
CUSTOM_CSS = """
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .result-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .example-box {
        background-color: #e8f4fd;
        padding: 0.8rem;
        border-radius: 0.3rem;
        margin: 0.5rem 0;
        border-left: 3px solid #1f77b4;
    }
    .metric-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
        border: 1px solid #dee2e6;
    }
</style>
"""

# Example queries organized by category
EXAMPLE_QUERIES = {
    "trading_orders": [
        "Buy 250 AAPL in account capers",
        "Sell 500 TSLA in accounts capers, ushy and halifax",
        "Increase exposure to AAPL by 0.5%",
        "Decrease exposure to RIVN by 0.3% in accounts ushy, melagg"
    ],
    "portfolio_holdings": [
        "What are my holdings in account ABC as of today",
        "Show me positions of TSLA in my account CAPERS",
        "What's my exposure to MSFT in accounts HALIFAX, MANIFAX",
        "Show change of my positions between 01-Jan-2024 to 31-Mar-2024"
    ],
    "performance_analysis": [
        "What are my returns in account capers, ushy",
        "Show performance of all accounts YTD",
        "Compare returns between accounts A and B"
    ]
}

# UI text constants
UI_TEXT = {
    "main_title": "📊 P.O.M.S",
    "subtitle": "Portfolio and OMS System",
    "query_placeholder": "e.g., 'Buy 100 shares of AAPL in account capers' or 'Show my holdings in account ABC as of today'",
    "query_help": "Ask questions about trading orders, portfolio holdings, or performance analysis",
    "footer_text": "P.O.M.S - Portfolio and OMS System | Powered by LangChain & OpenAI"
}

def configure_page():
    """Configure Streamlit page settings and apply custom CSS."""
    st.set_page_config(**PAGE_CONFIG)
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
