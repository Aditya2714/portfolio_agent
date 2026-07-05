from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.stock_tools import PortfolioManager, StockDataTool, CalculatorTool
from agents.portfolio_agents import PortfolioAgent
from agents.extra_agents import SentimentAgent, TechnicalAgent, TaxAgent, AlertAgent, CompareAgent

app = FastAPI(title="Portfolio Agent API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize tools
portfolio_manager = PortfolioManager()
stock_tool = StockDataTool()
calc_tool = CalculatorTool()
agent = PortfolioAgent()
sentiment_agent = SentimentAgent()
technical_agent = TechnicalAgent()
tax_agent = TaxAgent()
alert_agent = AlertAgent()
compare_agent = CompareAgent()


# Models
class HoldingRequest(BaseModel):
    symbol: str
    shares: float
    avg_cost: float

class CompareRequest(BaseModel):
    symbols: list[str]

class AIRequest(BaseModel):
    query: str
    portfolio: dict = None

class AlertRequest(BaseModel):
    symbol: str
    alert_type: str
    target_price: float


# Portfolio endpoints
@app.get("/api/portfolio")
def get_portfolio():
    return portfolio_manager.get_portfolio_summary()

@app.post("/api/portfolio/holdings")
def add_holding(holding: HoldingRequest):
    return portfolio_manager.add_holding(holding.symbol, holding.shares, holding.avg_cost)

@app.delete("/api/portfolio/holdings/{symbol}")
def remove_holding(symbol: str):
    return portfolio_manager.remove_holding(symbol)


# Stock endpoints
@app.get("/api/stock/{symbol}")
def get_stock_info(symbol: str):
    return stock_tool.get_stock_info(symbol)

@app.get("/api/stock/{symbol}/history")
def get_stock_history(symbol: str, period: str = "1y"):
    history = stock_tool.get_stock_history(symbol, period)
    return {"history": history.to_dict() if hasattr(history, 'to_dict') else []}


# Compare endpoint
@app.post("/api/compare")
def compare_stocks(req: CompareRequest):
    return compare_agent.compare_stocks(req.symbols)


# Sentiment endpoint
@app.get("/api/sentiment/{symbol}")
def get_sentiment(symbol: str):
    return sentiment_agent.analyze_sentiment(symbol)


# Technical endpoint
@app.get("/api/technical/{symbol}")
def get_technical(symbol: str):
    return technical_agent.analyze_technical(symbol)


# Tax endpoint
@app.post("/api/tax/analyze")
def analyze_tax(holdings: list[dict]):
    return tax_agent.analyze_tax_opportunities(holdings)


# Alert endpoints
@app.get("/api/alerts")
def get_alerts():
    return {"alerts": alert_agent.get_active_alerts() + alert_agent.get_triggered_alerts()}

@app.post("/api/alerts")
def add_alert(req: AlertRequest):
    return alert_agent.add_alert(req.symbol, req.alert_type, req.target_price)

@app.delete("/api/alerts/{alert_id}")
def remove_alert(alert_id: int):
    return alert_agent.remove_alert(alert_id)

@app.post("/api/alerts/check")
def check_alerts():
    return {"triggered": alert_agent.check_alerts()}


# AI endpoint
@app.post("/api/ai/analyze")
def ai_analyze(req: AIRequest):
    portfolio_summary = req.portfolio or portfolio_manager.get_portfolio_summary()
    result = agent.analyze(req.query, portfolio_summary)
    return {"response": result["response"]}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
