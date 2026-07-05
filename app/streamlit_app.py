import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.stock_tools import PortfolioManager, StockDataTool, CalculatorTool
from agents.portfolio_agents import PortfolioAgent
from agents.extra_agents import SentimentAgent, TechnicalAgent, TaxAgent, AlertAgent, CompareAgent

# Page config
st.set_page_config(
    page_title="AI Portfolio Manager",
    page_icon="💰",
    layout="wide"
)

# Initialize tools
@st.cache_resource
def load_tools():
    portfolio_manager = PortfolioManager()
    stock_tool = StockDataTool()
    calc_tool = CalculatorTool()
    agent = PortfolioAgent()
    return portfolio_manager, stock_tool, calc_tool, agent

portfolio_manager, stock_tool, calc_tool, agent = load_tools()

def main():
    st.title("💰 AI Portfolio Manager")
    st.markdown("### Your AI-Powered Financial Advisor")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", [
        "📊 Portfolio Overview",
        "🤖 AI Assistant",
        "➕ Manage Holdings",
        "📈 Stock Research",
        "⚖️ Compare Stocks",
        "📰 Sentiment Analysis",
        "📉 Technical Analysis",
        "💰 Tax Optimization",
        "🔔 Price Alerts",
        "📋 Reports"
    ])
    
    if page == "📊 Portfolio Overview":
        show_portfolio_overview()
    elif page == "🤖 AI Assistant":
        show_ai_assistant()
    elif page == "➕ Manage Holdings":
        show_manage_holdings()
    elif page == "📈 Stock Research":
        show_stock_research()
    elif page == "⚖️ Compare Stocks":
        show_compare_stocks()
    elif page == "📰 Sentiment Analysis":
        show_sentiment_analysis()
    elif page == "📉 Technical Analysis":
        show_technical_analysis()
    elif page == "💰 Tax Optimization":
        show_tax_optimization()
    elif page == "🔔 Price Alerts":
        show_price_alerts()
    elif page == "📋 Reports":
        show_reports()

def show_portfolio_overview():
    """Display portfolio overview with charts."""
    
    st.header("Portfolio Overview")
    
    summary = portfolio_manager.get_portfolio_summary()
    
    # Top metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Value", f"${summary['total_value']:,.2f}")
    
    with col2:
        st.metric("Invested", f"${summary['invested_value']:,.2f}")
    
    with col3:
        st.metric("Cash", f"${summary['cash']:,.2f}")
    
    with col4:
        st.metric("Total Return", f"{summary['total_return_pct']}%")
    
    st.divider()
    
    if not summary['holdings']:
        st.info("No holdings yet. Go to 'Manage Holdings' to add stocks.")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Asset Allocation")
        allocation = summary['allocation']
        
        fig = px.pie(
            values=list(allocation.values()),
            names=list(allocation.keys()),
            title="Portfolio Distribution",
            hole=0.3
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Holdings Performance")
        
        holdings_data = []
        for holding in summary['holdings']:
            returns = stock_tool.calculate_returns(holding['symbol'])
            holdings_data.append({
                'Symbol': holding['symbol'],
                'Shares': holding['shares'],
                'Value': holding['value'],
                'Return': returns.get('total_return_pct', 0)
            })
        
        df = pd.DataFrame(holdings_data)
        
        fig = px.bar(
            df,
            x='Symbol',
            y='Value',
            color='Return',
            color_continuous_scale=['red', 'yellow', 'green'],
            title="Holdings Value by Stock"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Risk Assessment
    st.subheader("Risk Assessment")
    risk = summary['risk']
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Risk Score", f"{risk['risk_score']}/10")
    
    with col2:
        st.metric("Risk Level", risk['risk_level'])
    
    with col3:
        st.metric("Volatility", f"{risk['avg_volatility']}%")

def show_ai_assistant():
    """AI assistant interface."""
    
    st.header("🤖 AI Portfolio Assistant")
    st.markdown("Ask me anything about your portfolio or investments!")
    
    # Chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # User input
    if prompt := st.chat_input("Ask about your portfolio..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get portfolio summary
        summary = portfolio_manager.get_portfolio_summary()
        
        # Run AI agent
        with st.chat_message("assistant"):
            with st.spinner("Analyzing..."):
                try:
                    result = agent.analyze(prompt, summary)
                    response = result['response']
                except Exception as e:
                    response = f"I encountered an error: {str(e)}. Please make sure your OpenAI API key is set."
            
            st.markdown(response)
        
        # Add assistant response
        st.session_state.messages.append({"role": "assistant", "content": response})

def show_manage_holdings():
    """Manage portfolio holdings."""
    
    st.header("Manage Holdings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Add New Holding")
        
        symbol = st.text_input("Stock Symbol", placeholder="AAPL")
        shares = st.number_input("Number of Shares", min_value=1, value=10)
        avg_cost = st.number_input("Average Cost per Share ($)", min_value=0.01, value=150.00)
        
        if st.button("Add Holding", type="primary"):
            if symbol:
                result = portfolio_manager.add_holding(symbol, shares, avg_cost)
                st.success(f"Added {symbol.upper()} to portfolio!")
                st.rerun()
    
    with col2:
        st.subheader("Remove Holding")
        
        holdings = portfolio_manager.portfolio["holdings"]
        if holdings:
            symbols = [h["symbol"] for h in holdings]
            remove_symbol = st.selectbox("Select Stock to Remove", symbols)
            
            if st.button("Remove Holding", type="secondary"):
                portfolio_manager.remove_holding(remove_symbol)
                st.success(f"Removed {remove_symbol} from portfolio!")
                st.rerun()
        else:
            st.info("No holdings to remove.")
    
    st.divider()
    
    # Current Holdings
    st.subheader("Current Holdings")
    
    if holdings:
        holdings_data = []
        for h in holdings:
            stock_info = stock_tool.get_stock_info(h["symbol"])
            current_price = stock_info.get("current_price", 0)
            value = current_price * h["shares"]
            pnl = (current_price - h["avg_cost"]) * h["shares"]
            
            holdings_data.append({
                'Symbol': h["symbol"],
                'Shares': h["shares"],
                'Avg Cost': f"${h['avg_cost']:.2f}",
                'Current Price': f"${current_price:.2f}",
                'Value': f"${value:,.2f}",
                'P&L': f"${pnl:,.2f}",
                'Date Added': h.get("date_added", "N/A")
            })
        
        df = pd.DataFrame(holdings_data)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No holdings in portfolio.")

def show_stock_research():
    """Research individual stocks."""
    
    st.header("Stock Research")
    
    symbol = st.text_input("Enter Stock Symbol", placeholder="AAPL")
    
    if symbol:
        with st.spinner("Fetching data..."):
            stock_info = stock_tool.get_stock_info(symbol)
            returns = stock_tool.calculate_returns(symbol)
            history = stock_tool.get_stock_history(symbol, "1y")
        
        if "error" not in stock_info:
            # Stock Info
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Current Price", f"${stock_info['current_price']:.2f}")
            
            with col2:
                st.metric("Market Cap", f"${stock_info['market_cap']/1e9:.2f}B")
            
            with col3:
                st.metric("P/E Ratio", f"{stock_info['pe_ratio']:.2f}")
            
            with col4:
                st.metric("52W High", f"${stock_info['52_week_high']:.2f}")
            
            st.divider()
            
            # Price Chart
            st.subheader("Price History (1 Year)")
            
            fig = go.Figure(data=[go.Candlestick(
                x=history.index,
                open=history['Open'],
                high=history['High'],
                low=history['Low'],
                close=history['Close']
            )])
            
            fig.update_layout(
                title=f"{symbol.upper()} Stock Price",
                xaxis_title="Date",
                yaxis_title="Price ($)",
                template="plotly_dark"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Returns Analysis
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Returns Analysis")
                st.metric("Total Return (1Y)", f"{returns.get('total_return_pct', 0)}%")
                st.metric("Volatility", f"{returns.get('volatility_pct', 0)}%")
            
            with col2:
                st.subheader("Company Info")
                st.write(f"**Name:** {stock_info['name']}")
                st.write(f"**Sector:** {stock_info['sector']}")
                st.write(f"**Industry:** {stock_info['industry']}")
                st.write(f"**Dividend Yield:** {stock_info['dividend_yield']*100:.2f}%")
        else:
            st.error(f"Error fetching data: {stock_info['error']}")

def show_sentiment_analysis():
    """Show news sentiment analysis for stocks."""
    
    st.header("📰 Sentiment Analysis")
    st.markdown("Analyze news sentiment for your stocks")
    
    sentiment_agent = SentimentAgent()
    
    # Get holdings
    summary = portfolio_manager.get_portfolio_summary()
    holdings = summary.get('holdings', [])
    
    if not holdings:
        st.info("Add holdings to see sentiment analysis.")
        return
    
    # Select stock
    symbols = [h['symbol'] for h in holdings]
    selected_symbol = st.selectbox("Select Stock", symbols)
    
    if st.button("Analyze Sentiment", type="primary"):
        with st.spinner("Analyzing news sentiment..."):
            result = sentiment_agent.analyze_sentiment(selected_symbol)
        
        # Display results
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Sentiment Score", f"{result['sentiment_score']}")
        
        with col2:
            st.metric("Sentiment", result['sentiment_label'])
        
        with col3:
            st.metric("News Count", result['news_count'])
        
        st.divider()
        
        # Sentiment breakdown
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Positive News", result['positive_news'], "📈")
        
        with col2:
            st.metric("Negative News", result['negative_news'], "📉")
        
        with col3:
            st.metric("Neutral News", result['neutral_news'], "➡️")
        
        st.divider()
        
        # Top headlines
        st.subheader("Top Headlines")
        for headline in result['top_headlines']:
            st.write(f"• {headline}")
        
        st.divider()
        
        # Recommendation
        st.subheader("Recommendation")
        st.info(result['recommendation'])

def show_technical_analysis():
    """Show technical analysis for stocks."""
    
    st.header("📉 Technical Analysis")
    st.markdown("Analyze technical indicators for your stocks")
    
    technical_agent = TechnicalAgent()
    
    # Get holdings
    summary = portfolio_manager.get_portfolio_summary()
    holdings = summary.get('holdings', [])
    
    if not holdings:
        st.info("Add holdings to see technical analysis.")
        return
    
    # Select stock
    symbols = [h['symbol'] for h in holdings]
    selected_symbol = st.selectbox("Select Stock", symbols)
    
    if st.button("Analyze Technicals", type="primary"):
        with st.spinner("Analyzing technical indicators..."):
            result = technical_agent.analyze_technical(selected_symbol)
        
        if "error" not in result:
            # Key metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Current Price", f"${result['current_price']:.2f}")
            
            with col2:
                st.metric("RSI", f"{result['rsi']:.2f}")
            
            with col3:
                st.metric("MACD", f"{result['macd']:.2f}")
            
            with col4:
                st.metric("Overall Rating", result['overall_rating'])
            
            st.divider()
            
            # Technical indicators
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Moving Averages")
                st.write(f"**SMA 20:** ${result['sma_20']:.2f} ({result['price_vs_sma20']})")
                st.write(f"**SMA 50:** ${result['sma_50']:.2f} ({result['price_vs_sma50']})")
                st.write(f"**Trend:** {result['sma_trend']}")
            
            with col2:
                st.subheader("Signals")
                st.write(f"**RSI Signal:** {result['rsi_signal']}")
                st.write(f"**MACD Signal:** {result['macd_signal']}")
                st.write(f"**Support:** ${result['support_level']:.2f}")
                st.write(f"**Resistance:** ${result['resistance_level']:.2f}")
        else:
            st.error(result['error'])

def show_compare_stocks():
    """Compare multiple stocks side-by-side."""
    
    st.header("⚖️ Compare Stocks")
    st.markdown("Compare multiple stocks side-by-side")
    
    compare_agent = CompareAgent()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        symbols_input = st.text_input(
            "Enter stock symbols (comma-separated)",
            placeholder="AAPL, MSFT, GOOGL"
        )
    
    with col2:
        st.write("")
        st.write("")
        compare_button = st.button("Compare", type="primary", use_container_width=True)
    
    # Quick add from holdings
    summary = portfolio_manager.get_portfolio_summary()
    holdings = summary.get('holdings', [])
    
    if holdings:
        st.markdown("**Or select from your holdings:**")
        holding_symbols = [h['symbol'] for h in holdings]
        selected_holdings = st.multiselect("Select stocks", holding_symbols, key="compare_holdings")
        
        if selected_holdings:
            symbols_input = ", ".join(selected_holdings)
    
    if compare_button and symbols_input:
        symbols = [s.strip().upper() for s in symbols_input.split(",") if s.strip()]
        
        if len(symbols) < 2:
            st.warning("Please enter at least 2 stock symbols.")
            return
        
        with st.spinner(f"Comparing {len(symbols)} stocks..."):
            result = compare_agent.compare_stocks(symbols)
        
        if result['stocks']:
            # Main comparison table
            st.subheader("📊 Comparison Overview")
            
            # Create comparison dataframe
            comparison_data = []
            for stock in result['stocks']:
                comparison_data.append({
                    'Stock': f"{stock['symbol']}",
                    'Name': stock['name'],
                    'Price': f"${stock['current_price']:.2f}",
                    'Market Cap': stock['market_capformatted'],
                    'P/E Ratio': stock['pe_ratio'],
                    'Dividend': f"{stock['dividend_yield']}%",
                    '1Y Return': f"{stock['year_return']}%",
                    'Volatility': f"{stock['volatility']}%"
                })
            
            df = pd.DataFrame(comparison_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            st.divider()
            
            # Detailed metrics
            st.subheader("📈 Detailed Metrics")
            
            for stock in result['stocks']:
                with st.expander(f"{stock['symbol']} - {stock['name']}"):
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Price", f"${stock['current_price']:.2f}")
                        st.metric("P/E Ratio", stock['pe_ratio'])
                    
                    with col2:
                        st.metric("Market Cap", stock['market_capformatted'])
                        st.metric("Forward P/E", stock['forward_pe'])
                    
                    with col3:
                        st.metric("1Y Return", f"{stock['year_return']}%")
                        st.metric("Quarter Return", f"{stock['quarter_return']}%")
                    
                    with col4:
                        st.metric("Dividend Yield", f"{stock['dividend_yield']}%")
                        st.metric("Volatility", f"{stock['volatility']}%")
                    
                    st.divider()
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write(f"**Sector:** {stock['sector']}")
                        st.write(f"**Industry:** {stock['industry']}")
                    
                    with col2:
                        st.write(f"**Beta:** {stock['beta']}")
                        st.write(f"**Profit Margin:** {stock['profit_margin']}%")
                    
                    with col3:
                        st.write(f"**Revenue Growth:** {stock['revenue_growth']}%")
                        st.write(f"**ROE:** {stock['roe']}%")
                    
                    # 52-week range
                    st.progress(stock['price_vs_52w'] / 100)
                    st.caption(f"52-Week Range: ${stock['low_52w']} - ${stock['high_52w']} (Current: {stock['price_vs_52w']}% of range)")
            
            st.divider()
            
            # Category winners
            st.subheader("🏆 Category Winners")
            
            if result['winners']:
                category_names = {
                    "best_value": "Best Value (Low P/E)",
                    "best_growth": "Best Growth",
                    "best_return": "Best 1-Year Return",
                    "lowest_risk": "Lowest Risk",
                    "best_dividend": "Best Dividend",
                    "most_profitable": "Most Profitable",
                    "best_roe": "Best ROE"
                }
                
                num_winners = len(result['winners'])
                cols = st.columns(min(num_winners, 7))
                for idx, (category, symbol) in enumerate(result['winners'].items()):
                    with cols[idx]:
                        st.metric(category_names.get(category, category), symbol)
            else:
                st.info("No category winners determined.")
            
            st.divider()
            
            # Overall recommendation
            st.subheader("📋 Recommendation")
            st.markdown(result['recommendation'])
            
            # Visual comparison chart
            st.subheader("📊 Visual Comparison")
            
            chart_data = pd.DataFrame({
                'Stock': [s['symbol'] for s in result['stocks']],
                '1Y Return (%)': [s['year_return'] for s in result['stocks']],
                'Dividend Yield (%)': [s['dividend_yield'] for s in result['stocks']],
                'Profit Margin (%)': [s['profit_margin'] if isinstance(s['profit_margin'], (int, float)) else 0 for s in result['stocks']]
            })
            
            fig = px.bar(chart_data, x='Stock', y=['1Y Return (%)', 'Dividend Yield (%)', 'Profit Margin (%)'],
                         barmode='group', template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
        
        else:
            st.error("Could not fetch data for the specified stocks.")
    
    elif compare_button:
        st.warning("Please enter stock symbols to compare.")

def show_tax_optimization():
    """Show tax optimization suggestions."""
    
    st.header("💰 Tax Optimization")
    st.markdown("Find tax-loss harvesting opportunities")
    
    tax_agent = TaxAgent()
    
    # Get holdings
    summary = portfolio_manager.get_portfolio_summary()
    holdings = summary.get('holdings', [])
    
    if not holdings:
        st.info("Add holdings to see tax optimization.")
        return
    
    if st.button("Analyze Tax Opportunities", type="primary"):
        with st.spinner("Analyzing tax opportunities..."):
            result = tax_agent.analyze_tax_opportunities(holdings)
        
        # Summary
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Potential Tax Savings", f"${result['total_potential_savings']:,.2f}")
        
        with col2:
            st.metric("Tax Bracket", result['tax_brassack_assumption'])
        
        st.divider()
        
        # Opportunities
        st.subheader("Tax Opportunities")
        
        for opp in result['opportunities']:
            with st.expander(f"{opp['symbol']} - {'Loss' if 'unrealized_loss' in opp else 'Gain'}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Shares:** {opp['shares']}")
                    st.write(f"**Avg Cost:** ${opp['avg_cost']:.2f}")
                    st.write(f"**Current Price:** ${opp['current_price']:.2f}")
                
                with col2:
                    if 'unrealized_loss' in opp:
                        st.write(f"**Unrealized Loss:** ${opp['unrealized_loss']:,.2f}")
                        st.write(f"**Potential Savings:** ${opp['potential_tax_savings']:,.2f}")
                    else:
                        st.write(f"**Unrealized Gain:** ${opp['unrealized_gain']:,.2f}")
                        st.write(f"**Tax Liability:** ${opp['potential_tax_liability']:,.2f}")
                
                st.info(opp['recommendation'])
        
        st.divider()
        
        # Overall recommendation
        st.subheader("Recommendation")
        st.info(result['recommendation'])

def show_price_alerts():
    """Manage price alerts."""
    
    st.header("🔔 Price Alerts")
    st.markdown("Set alerts for your target prices")
    
    alert_agent = AlertAgent()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Add New Alert")
        
        symbol = st.text_input("Stock Symbol", placeholder="AAPL")
        alert_type = st.selectbox("Alert Type", ["Above", "Below"])
        target_price = st.number_input("Target Price ($)", min_value=0.01, value=200.00)
        
        if st.button("Add Alert", type="primary"):
            if symbol:
                result = alert_agent.add_alert(symbol, alert_type.lower(), target_price)
                st.success(f"Alert added for {symbol.upper()}!")
                st.rerun()
    
    with col2:
        st.subheader("Active Alerts")
        
        active_alerts = alert_agent.get_active_alerts()
        
        if active_alerts:
            for alert in active_alerts:
                with st.expander(f"{alert['symbol']} - {alert['alert_type'].title()} ${alert['target_price']:.2f}"):
                    st.write(f"**Created:** {alert['created_at']}")
                    if st.button("Remove", key=f"remove_{alert['id']}"):
                        alert_agent.remove_alert(alert['id'])
                        st.rerun()
        else:
            st.info("No active alerts.")
    
    st.divider()
    
    # Check triggered alerts
    st.subheader("Triggered Alerts")
    
    if st.button("Check Alerts"):
        triggered = alert_agent.check_alerts()
        
        if triggered:
            for alert in triggered:
                st.warning(alert['message'])
        else:
            st.info("No alerts triggered yet.")
    
    # Show triggered alerts history
    triggered_alerts = alert_agent.get_triggered_alerts()
    
    if triggered_alerts:
        st.subheader("Alert History")
        for alert in triggered_alerts:
            st.write(f"• {alert['symbol']} reached ${alert['target_price']:.2f}")

def show_reports():
    """Generate and display reports."""
    
    st.header("Portfolio Reports")
    
    summary = portfolio_manager.get_portfolio_summary()
    
    # Executive Summary
    st.subheader("Executive Summary")
    
    st.info(f"""
    **Portfolio Value:** ${summary['total_value']:,.2f}
    
    **Total Return:** {summary['total_return_pct']}%
    
    **Risk Level:** {summary['risk']['risk_level']}
    
    **Number of Holdings:** {len(summary['holdings'])}
    """)
    
    # Recommendations
    st.subheader("AI Recommendations")
    
    if summary['holdings']:
        with st.spinner("Generating recommendations..."):
            try:
                result = agent.analyze(
                    "Provide investment recommendations for my portfolio",
                    summary
                )
                st.markdown(result['response'])
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.info("Add holdings to get personalized recommendations.")

if __name__ == "__main__":
    main()
