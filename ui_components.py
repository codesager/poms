"""
UI Components for P.O.M.S - Portfolio and OMS System
"""
import streamlit as st
from typing import List, Any
from pots_models import Order, PortfolioHolding, PortfolioPerformance
from config import UI_TEXT, EXAMPLE_QUERIES

def render_header():
    """Render the main header section."""
    st.markdown(f'<h1 class="main-header">{UI_TEXT["main_title"]}</h1>', unsafe_allow_html=True)
    #st.markdown(f'<p class="sub-header">{UI_TEXT["subtitle"]}</p>', unsafe_allow_html=True)

def render_sidebar():
    """Render the sidebar with example queries."""
    with st.sidebar:
        st.header("💡 Example Queries")
        
        # Trading Orders section
        st.subheader("Trading Orders")
        for example in EXAMPLE_QUERIES["trading_orders"]:
            if st.button(f"📝 {example}", key=f"order_{example}"):
                st.session_state.query_text = example
        
        # Portfolio Holdings section
        st.subheader("Portfolio Holdings")
        for example in EXAMPLE_QUERIES["portfolio_holdings"]:
            if st.button(f"📊 {example}", key=f"holding_{example}"):
                st.session_state.query_text = example
        
        # Performance Analysis section
        st.subheader("Performance Analysis")
        for example in EXAMPLE_QUERIES["performance_analysis"]:
            if st.button(f"📈 {example}", key=f"perf_{example}"):
                st.session_state.query_text = example

def render_query_input():
    """Render the query input section."""
    query_text = st.text_area(
        "Enter your portfolio query:",
        value=st.session_state.get('query_text', ''),
        height=100,
        placeholder=UI_TEXT["query_placeholder"],
        help=UI_TEXT["query_help"]
    )
    return query_text

def render_footer():
    """Render the footer section."""
    st.markdown("---")
    st.markdown(
        f"""
        <div style='text-align: center; color: #666;'>
            <p>{UI_TEXT["footer_text"]}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def display_order_result(orders: List[Order]):
    """Display order results in a formatted way."""
    if not orders:
        st.warning("No orders found")
        return
    
    st.subheader("📋 Trading Orders")
    
    for i, order in enumerate(orders, 1):
        with st.expander(f"Order {i}: {order.action.upper()} {order.ticker or 'Multiple Assets'}", expanded=True):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Action", order.action.upper())
                st.metric("Ticker", order.ticker or "N/A")
            
            with col2:
                if order.quantity:
                    st.metric("Quantity", f"{order.quantity:,}")
                else:
                    st.metric("Quantity", "N/A")
                
                if order.weight:
                    st.metric("Weight", f"{order.weight:.2f}%")
                else:
                    st.metric("Weight", "N/A")
            
            with col3:
                if order.accounts:
                    st.metric("Accounts", len(order.accounts))
                    st.write("**Account List:**")
                    for account in order.accounts:
                        st.write(f"• {account}")
                else:
                    st.metric("Accounts", "All Accounts")

def display_holding_result(holdings: List[PortfolioHolding]):
    """Display portfolio holdings results in a formatted way."""
    if not holdings:
        st.warning("No holdings found")
        return
    
    st.subheader("📊 Portfolio Holdings")
    
    for i, holding in enumerate(holdings, 1):
        with st.expander(f"Holding {i}: {holding.ticker or 'All Holdings'}", expanded=True):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Ticker", holding.ticker or "All")
                if holding.fields:
                    st.write("**Fields:**")
                    for field in holding.fields:
                        st.write(f"• {field}")
                else:
                    st.write("**Fields:** All available")
            
            with col2:
                st.metric("Start Date", holding.start_date)
                st.metric("End Date", holding.end_date or "N/A")
            
            with col3:
                if holding.accounts:
                    st.metric("Accounts", len(holding.accounts))
                    st.write("**Account List:**")
                    for account in holding.accounts:
                        st.write(f"• {account}")
                else:
                    st.metric("Accounts", "All Accounts")

def display_performance_result(performances: List[PortfolioPerformance]):
    """Display portfolio performance results in a formatted way."""
    if not performances:
        st.warning("No performance data found")
        return
    
    st.subheader("📈 Portfolio Performance")
    
    for i, performance in enumerate(performances, 1):
        with st.expander(f"Performance {i}: {performance.accounts or 'All Accounts'}", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Start Date", performance.start_date)
                st.metric("End Date", performance.end_date)
            
            with col2:
                st.metric("Accounts", performance.accounts or "All Accounts")

def display_raw_result(result: Any):
    """Display raw JSON result."""
    st.subheader("🔍 Raw Result")
    st.json(result.model_dump() if hasattr(result, 'model_dump') else result)

def display_results(result: Any):
    """Display results based on the result type."""
    if result is None:
        st.warning("I couldn't understand your query. Please try rephrasing or use one of the example queries from the sidebar.")
        return
    
    st.success("Query processed successfully!")
    
    # Display results based on type
    if hasattr(result, 'orders') and result.orders:
        display_order_result(result.orders)
    elif hasattr(result, 'holdings') and result.holdings:
        display_holding_result(result.holdings)
    elif hasattr(result, 'performances') and result.performances:
        display_performance_result(result.performances)
    else:
        st.info("No specific data extracted. Here's the raw result:")
        display_raw_result(result)
    
    # Show raw JSON in expander
    with st.expander("🔍 View Raw JSON", expanded=False):
        st.json(result.model_dump() if hasattr(result, 'model_dump') else result)
