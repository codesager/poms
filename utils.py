"""
Utility functions for P.O.M.S - Portfolio and OMS System
"""
import streamlit as st
from typing import Any
from pots_models import route_input_and_extract

def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'query_text' not in st.session_state:
        st.session_state.query_text = ""

def process_query(query_text: str) -> Any:
    """
    Process a query using the routing and extraction system.
    
    Args:
        query_text: The user's query text
        
    Returns:
        The extracted result or None if processing failed
    """
    if not query_text.strip():
        st.warning("Please enter a query to process.")
        return None
    
    try:
        with st.spinner("Processing your query..."):
            result = route_input_and_extract(query_text)
            return result
    except Exception as e:
        st.error(f"An error occurred while processing your query: {str(e)}")
        st.exception(e)
        return None

def handle_query_processing(query_text: str):
    """
    Handle the complete query processing workflow.
    
    Args:
        query_text: The user's query text
    """
    if query_text.strip():
        result = process_query(query_text)
        return result
    else:
        st.warning("Please enter a query to process.")
        return None
