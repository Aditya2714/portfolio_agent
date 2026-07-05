import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os

class StockDataTool:
    """Tool for fetching stock market data."""
    
    def get_stock_info(self, symbol: str) -> dict:
        """Get basic stock information."""
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            
            return {
                "symbol": symbol,
                "name": info.get("longName", "N/A"),
                "current_price": info.get("currentPrice", 0),
                "previous_close": info.get("previousClose", 0),
                "market_cap": info.get("marketCap", 0),
                "pe_ratio": info.get("trailingPE", 0),
                "dividend_yield": info.get("dividendYield", 0),
                "52_week_high": info.get("fiftyTwoWeekHigh", 0),
                "52_week_low": info.get("fiftyTwoWeekLow", 0),
                "volume": info.get("volume", 0),
                "avg_volume": info.get("averageVolume", 0),
                "sector": info.get("sector", "N/A"),
                "industry": info.get("industry", "N/A")
            }
        except Exception as e:
            return {"error": str(e)}
    
    def get_stock_history(self, symbol: str, period: str = "1y") -> pd.DataFrame:
        """Get historical stock data."""
        try:
            stock = yf.Ticker(symbol)
            history = stock.history(period=period)
            return history
        except Exception as e:
            return pd.DataFrame()
    
    def calculate_returns(self, symbol: str, period: str = "1y") -> dict:
        """Calculate stock returns over a period."""
        try:
            history = self.get_stock_history(symbol, period)
            if history.empty:
                return {"error": "No data found"}
            
            current_price = history['Close'].iloc[-1]
            start_price = history['Close'].iloc[0]
            
            total_return = ((current_price - start_price) / start_price) * 100
            
            # Calculate volatility
            daily_returns = history['Close'].pct_change().dropna()
            volatility = daily_returns.std() * np.sqrt(252) * 100
            
            return {
                "symbol": symbol,
                "start_price": round(start_price, 2),
                "current_price": round(current_price, 2),
                "total_return_pct": round(total_return, 2),
                "volatility_pct": round(volatility, 2),
                "period": period
            }
        except Exception as e:
            return {"error": str(e)}
    
    def get_market_summary(self) -> dict:
        """Get major market indices summary."""
        indices = {
            "^GSPC": "S&P 500",
            "^DJI": "Dow Jones",
            "^IXIC": "NASDAQ",
            "^VIX": "VIX (Volatility)"
        }
        
        summary = {}
        for symbol, name in indices.items():
            try:
                stock = yf.Ticker(symbol)
                info = stock.info
                summary[name] = {
                    "price": info.get("regularMarketPrice", 0),
                    "change": info.get("regularMarketChange", 0),
                    "change_pct": info.get("regularMarketChangePercent", 0)
                }
            except:
                summary[name] = {"price": 0, "change": 0, "change_pct": 0}
        
        return summary


class NewsTool:
    """Tool for fetching financial news (simulated)."""
    
    def get_stock_news(self, symbol: str) -> list:
        """Get news for a stock (simulated for demo)."""
        # In production, use NewsAPI or similar
        news = [
            {
                "title": f"{symbol} Reports Strong Quarterly Earnings",
                "summary": f"{symbol} beat analyst expectations with revenue growth of 15%.",
                "sentiment": "positive",
                "source": "Financial Times",
                "date": datetime.now().strftime("%Y-%m-%d")
            },
            {
                "title": f"Market Analysis: {symbol} Outlook",
                "summary": f"Analysts maintain buy rating for {symbol} with price target increase.",
                "sentiment": "positive",
                "source": "Bloomberg",
                "date": datetime.now().strftime("%Y-%m-%d")
            },
            {
                "title": f"Sector Trends Affecting {symbol}",
                "summary": f"Industry trends suggest continued growth for {symbol}'s market segment.",
                "sentiment": "neutral",
                "source": "Reuters",
                "date": datetime.now().strftime("%Y-%m-%d")
            }
        ]
        return news
    
    def get_market_news(self) -> list:
        """Get general market news (simulated)."""
        news = [
            {
                "title": "Fed Signals Potential Rate Cut",
                "summary": "Federal Reserve hints at rate reduction in upcoming meeting.",
                "sentiment": "positive"
            },
            {
                "title": "Tech Stocks Rally Continues",
                "summary": "Technology sector leads market gains for third consecutive day.",
                "sentiment": "positive"
            },
            {
                "title": "Global Markets Mixed",
                "summary": "Asian markets up, European markets flat amid trade concerns.",
                "sentiment": "neutral"
            }
        ]
        return news


class CalculatorTool:
    """Tool for financial calculations."""
    
    def calculate_portfolio_value(self, holdings: list) -> dict:
        """Calculate total portfolio value."""
        stock_tool = StockDataTool()
        total_value = 0
        holdings_detail = []
        
        for holding in holdings:
            symbol = holding["symbol"]
            shares = holding["shares"]
            
            stock_info = stock_tool.get_stock_info(symbol)
            current_price = stock_info.get("current_price", 0)
            value = current_price * shares
            total_value += value
            
            holdings_detail.append({
                "symbol": symbol,
                "shares": shares,
                "current_price": current_price,
                "value": value
            })
        
        return {
            "total_value": total_value,
            "holdings": holdings_detail
        }
    
    def calculate_asset_allocation(self, holdings: list) -> dict:
        """Calculate asset allocation percentages."""
        portfolio = self.calculate_portfolio_value(holdings)
        total = portfolio["total_value"]
        
        allocation = {}
        for holding in portfolio["holdings"]:
            symbol = holding["symbol"]
            percentage = (holding["value"] / total) * 100 if total > 0 else 0
            allocation[symbol] = round(percentage, 2)
        
        return allocation
    
    def calculate_risk_score(self, holdings: list) -> dict:
        """Calculate portfolio risk score."""
        stock_tool = StockDataTool()
        
        volatilities = []
        for holding in holdings:
            returns = stock_tool.calculate_returns(holding["symbol"])
            if "volatility_pct" in returns:
                volatilities.append(returns["volatility_pct"])
        
        if not volatilities:
            return {"risk_score": 0, "risk_level": "Unknown"}
        
        avg_volatility = np.mean(volatilities)
        
        # Risk scoring: 0-10 scale
        if avg_volatility < 15:
            risk_score = 3
            risk_level = "Low"
        elif avg_volatility < 25:
            risk_score = 5
            risk_level = "Moderate"
        elif avg_volatility < 35:
            risk_score = 7
            risk_level = "High"
        else:
            risk_score = 9
            risk_level = "Very High"
        
        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "avg_volatility": round(avg_volatility, 2)
        }


class PortfolioManager:
    """Main portfolio management tool."""
    
    def __init__(self, data_file="data/portfolio.json"):
        self.data_file = data_file
        self.load_portfolio()
    
    def load_portfolio(self):
        """Load portfolio from file."""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                self.portfolio = json.load(f)
        else:
            self.portfolio = {
                "name": "My Portfolio",
                "holdings": [],
                "cash": 10000
            }
            self.save_portfolio()
    
    def save_portfolio(self):
        """Save portfolio to file."""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w') as f:
            json.dump(self.portfolio, f, indent=2)
    
    def add_holding(self, symbol: str, shares: int, avg_cost: float):
        """Add a stock to portfolio."""
        # Check if already exists
        for holding in self.portfolio["holdings"]:
            if holding["symbol"] == symbol.upper():
                holding["shares"] += shares
                holding["avg_cost"] = ((holding["avg_cost"] * (holding["shares"] - shares)) + 
                                       (avg_cost * shares)) / holding["shares"]
                self.save_portfolio()
                return {"status": "updated", "symbol": symbol.upper()}
        
        # Add new holding
        self.portfolio["holdings"].append({
            "symbol": symbol.upper(),
            "shares": shares,
            "avg_cost": avg_cost,
            "date_added": datetime.now().strftime("%Y-%m-%d")
        })
        self.save_portfolio()
        return {"status": "added", "symbol": symbol.upper()}
    
    def remove_holding(self, symbol: str):
        """Remove a stock from portfolio."""
        self.portfolio["holdings"] = [
            h for h in self.portfolio["holdings"] 
            if h["symbol"] != symbol.upper()
        ]
        self.save_portfolio()
        return {"status": "removed", "symbol": symbol.upper()}
    
    def get_portfolio_summary(self) -> dict:
        """Get complete portfolio summary."""
        calc_tool = CalculatorTool()
        stock_tool = StockDataTool()
        
        if not self.portfolio["holdings"]:
            return {
                "total_value": self.portfolio["cash"],
                "invested_value": 0,
                "cash": self.portfolio["cash"],
                "total_invested": 0,
                "total_return_pct": 0,
                "holdings": [],
                "allocation": {},
                "risk": {"risk_score": 0, "risk_level": "Low", "avg_volatility": 0}
            }
        
        portfolio_value = calc_tool.calculate_portfolio_value(self.portfolio["holdings"])
        allocation = calc_tool.calculate_asset_allocation(self.portfolio["holdings"])
        risk = calc_tool.calculate_risk_score(self.portfolio["holdings"])
        
        total_invested = sum(
            h["shares"] * h["avg_cost"] 
            for h in self.portfolio["holdings"]
        )
        
        total_value = portfolio_value["total_value"] + self.portfolio["cash"]
        total_return = ((total_value - total_invested - self.portfolio["cash"]) / 
                       (total_invested + self.portfolio["cash"])) * 100 if (total_invested + self.portfolio["cash"]) > 0 else 0
        
        return {
            "total_value": total_value,
            "invested_value": portfolio_value["total_value"],
            "cash": self.portfolio["cash"],
            "total_invested": total_invested,
            "total_return_pct": round(total_return, 2),
            "holdings": portfolio_value["holdings"],
            "allocation": allocation,
            "risk": risk
        }
