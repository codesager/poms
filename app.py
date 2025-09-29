"""
Main application module for P.O.M.S - Portfolio and OMS System
"""
import streamlit as st
from config import configure_page
from ui_components import (
    render_header, 
    render_sidebar, 
    render_query_input, 
    render_footer, 
    display_results
)
from utils import initialize_session_state, handle_query_processing

def main():
    """Main application function."""
    # Configure page
    configure_page()
    
    # Initialize session state
    initialize_session_state()
    
    # Render header
    render_header()
    
    # Render sidebar
    render_sidebar()
    
    # Render query input
    query_text = render_query_input()
    
    # Process query
    if st.button("🚀 Process Query", type="primary"):
        result = handle_query_processing(query_text)
        if result is not None:
            display_results(result)
    
    # Render footer
    render_footer()

if __name__ == "__main__":
    main()
