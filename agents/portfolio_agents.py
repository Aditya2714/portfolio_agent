from groq import Groq
from dotenv import load_dotenv
import json
import os
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure Groq API
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class BaseAgent:
    """Base class for all agents."""
    
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
    
    def _generate(self, prompt: str) -> str:
        """Generate response using Groq (Llama 3.3)."""
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1024
        )
        return response.choices[0].message.content
    
    def think(self, input_data: dict) -> dict:
        """Process input and generate response."""
        raise NotImplementedError


class PlannerAgent(BaseAgent):
    """Agent that plans and coordinates the workflow."""
    
    def __init__(self):
        super().__init__("Planner", "Plans and coordinates the portfolio analysis workflow")
    
    def think(self, user_query: str, portfolio_summary: dict) -> dict:
        """Plan the analysis based on user query."""
        
        prompt = f"""You are a financial planning agent. Analyze the user's request and create a plan.

User Query: {user_query}

Current Portfolio Summary:
- Total Value: ${portfolio_summary.get('total_value', 0):,.2f}
- Holdings: {len(portfolio_summary.get('holdings', []))} stocks
- Risk Level: {portfolio_summary.get('risk', {}).get('risk_level', 'Unknown')}

Create a plan with:
1. What information to gather
2. Which agents to use
3. What analysis to perform
4. What recommendations to make

Respond with a JSON object containing:
- "analysis_type": "portfolio_review" | "stock_analysis" | "risk_assessment" | "recommendation"
- "stocks_to_analyze": list of stock symbols
- "actions": list of actions to take
- "focus_areas": list of focus areas
"""
        
        response = self._generate(prompt)
        
        try:
            plan = json.loads(response)
        except:
            plan = {
                "analysis_type": "portfolio_review",
                "stocks_to_analyze": [h["symbol"] for h in portfolio_summary.get("holdings", [])],
                "actions": ["analyze_portfolio", "check_market", "generate_recommendations"],
                "focus_areas": ["performance", "risk", "allocation"]
            }
        
        return plan


class MarketAnalystAgent(BaseAgent):
    """Agent that analyzes market data."""
    
    def __init__(self):
        super().__init__("Market Analyst", "Analyzes market trends and stock performance")
        from tools.stock_tools import StockDataTool
        self.stock_tool = StockDataTool()
    
    def think(self, symbols: list) -> dict:
        """Analyze market data for given symbols."""
        
        analysis = {}
        for symbol in symbols:
            stock_info = self.stock_tool.get_stock_info(symbol)
            returns = self.stock_tool.calculate_returns(symbol)
            news = self.stock_tool.get_stock_history(symbol, "1mo")
            
            analysis[symbol] = {
                "info": stock_info,
                "returns": returns,
                "recent_trend": "up" if not news.empty and news['Close'].iloc[-1] > news['Close'].iloc[0] else "down"
            }
        
        # Get market summary
        market_summary = self.stock_tool.get_market_summary()
        
        return {
            "stock_analysis": analysis,
            "market_summary": market_summary,
            "timestamp": datetime.now().isoformat()
        }


class NewsAnalystAgent(BaseAgent):
    """Agent that analyzes financial news."""
    
    def __init__(self):
        super().__init__("News Analyst", "Analyzes financial news and sentiment")
        from tools.stock_tools import NewsTool
        self.news_tool = NewsTool()
    
    def think(self, symbols: list) -> dict:
        """Analyze news for given symbols."""
        
        news_analysis = {}
        for symbol in symbols:
            news = self.news_tool.get_stock_news(symbol)
            
            # Simple sentiment analysis
            positive = sum(1 for n in news if n["sentiment"] == "positive")
            negative = sum(1 for n in news if n["sentiment"] == "negative")
            neutral = sum(1 for n in news if n["sentiment"] == "neutral")
            
            if positive > negative:
                overall_sentiment = "positive"
            elif negative > positive:
                overall_sentiment = "negative"
            else:
                overall_sentiment = "neutral"
            
            news_analysis[symbol] = {
                "articles": news,
                "sentiment_breakdown": {
                    "positive": positive,
                    "negative": negative,
                    "neutral": neutral
                },
                "overall_sentiment": overall_sentiment
            }
        
        # Get market news
        market_news = self.news_tool.get_market_news()
        
        return {
            "stock_news": news_analysis,
            "market_news": market_news,
            "timestamp": datetime.now().isoformat()
        }


class RiskAgent(BaseAgent):
    """Agent that assesses portfolio risk."""
    
    def __init__(self):
        super().__init__("Risk Analyst", "Assesses portfolio risk and suggests mitigations")
        from tools.stock_tools import CalculatorTool
        self.calc_tool = CalculatorTool()
    
    def think(self, portfolio_summary: dict) -> dict:
        """Assess portfolio risk."""
        
        holdings = portfolio_summary.get("holdings", [])
        allocation = portfolio_summary.get("allocation", {})
        
        # Calculate concentration risk
        max_allocation = max(allocation.values()) if allocation else 0
        concentration_risk = "High" if max_allocation > 40 else "Moderate" if max_allocation > 25 else "Low"
        
        # Calculate diversification
        num_holdings = len(holdings)
        diversification = "Poor" if num_holdings < 3 else "Moderate" if num_holdings < 6 else "Good"
        
        # Get risk score
        risk_info = self.calc_tool.calculate_risk_score(holdings)
        
        # Generate risk recommendations
        recommendations = []
        if concentration_risk == "High":
            recommendations.append("Reduce concentration in single stock")
        if diversification == "Poor":
            recommendations.append("Add more diversified holdings")
        if risk_info.get("risk_level") == "High":
            recommendations.append("Consider adding defensive stocks or bonds")
        
        return {
            "risk_score": risk_info.get("risk_score", 0),
            "risk_level": risk_info.get("risk_level", "Unknown"),
            "concentration_risk": concentration_risk,
            "diversification": diversification,
            "volatility": risk_info.get("avg_volatility", 0),
            "recommendations": recommendations,
            "timestamp": datetime.now().isoformat()
        }


class SynthesizerAgent(BaseAgent):
    """Agent that synthesizes all information into final response."""
    
    def __init__(self):
        super().__init__("Synthesizer", "Combines all analysis into coherent recommendations")
    
    def think(self, user_query: str, market_data: dict, news_data: dict, 
              risk_data: dict, portfolio_summary: dict) -> str:
        """Generate final response combining all analysis."""
        
        prompt = f"""You are a senior financial advisor AI. Synthesize all the analysis below into a clear, 
        actionable response for the user.

User Query: {user_query}

Portfolio Summary:
- Total Value: ${portfolio_summary.get('total_value', 0):,.2f}
- Total Return: {portfolio_summary.get('total_return_pct', 0)}%
- Risk Level: {risk_data.get('risk_level', 'Unknown')}

Market Analysis:
{json.dumps(market_data.get('stock_analysis', {}), indent=2, default=str)}

News Analysis:
{json.dumps(news_data.get('stock_news', {}), indent=2, default=str)}

Risk Assessment:
- Risk Score: {risk_data.get('risk_score', 0)}/10
- Concentration Risk: {risk_data.get('concentration_risk', 'Unknown')}
- Diversification: {risk_data.get('diversification', 'Unknown')}

Provide:
1. Executive summary (2-3 sentences)
2. Key findings
3. Specific recommendations
4. Risk warnings
5. Next steps

Be professional, clear, and actionable.
"""
        
        response = self._generate(prompt)
        return response


class PortfolioAgent:
    """Main orchestrator agent that coordinates all sub-agents."""
    
    def __init__(self):
        self.planner = PlannerAgent()
        self.market_analyst = MarketAnalystAgent()
        self.news_analyst = NewsAnalystAgent()
        self.risk_agent = RiskAgent()
        self.synthesizer = SynthesizerAgent()
    
    def analyze(self, user_query: str, portfolio_summary: dict) -> dict:
        """Run complete analysis workflow."""
        
        # Step 1: Plan
        plan = self.planner.think(user_query, portfolio_summary)
        
        # Step 2: Gather market data
        market_data = self.market_analyst.think(plan.get("stocks_to_analyze", []))
        
        # Step 3: Gather news
        news_data = self.news_analyst.think(plan.get("stocks_to_analyze", []))
        
        # Step 4: Assess risk
        risk_data = self.risk_agent.think(portfolio_summary)
        
        # Step 5: Synthesize response
        final_response = self.synthesizer.think(
            user_query, market_data, news_data, risk_data, portfolio_summary
        )
        
        return {
            "response": final_response,
            "plan": plan,
            "market_data": market_data,
            "news_data": news_data,
            "risk_data": risk_data,
            "portfolio_summary": portfolio_summary
        }
