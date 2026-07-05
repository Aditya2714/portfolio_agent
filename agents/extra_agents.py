import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os

class SentimentAgent:
    """Agent that analyzes news sentiment for stocks."""
    
    def __init__(self):
        self.name = "Sentiment Analyst"
    
    def analyze_sentiment(self, symbol: str) -> dict:
        """Analyze news sentiment for a stock."""
        
        # Simulated news analysis (in production, use NewsAPI or similar)
        news_items = self._get_simulated_news(symbol)
        
        # Calculate sentiment scores
        positive_count = sum(1 for n in news_items if n["sentiment"] == "positive")
        negative_count = sum(1 for n in news_items if n["sentiment"] == "negative")
        neutral_count = sum(1 for n in news_items if n["sentiment"] == "neutral")
        total = len(news_items)
        
        # Calculate overall sentiment score (-1 to 1)
        sentiment_score = (positive_count - negative_count) / total if total > 0 else 0
        
        # Determine sentiment label
        if sentiment_score > 0.3:
            sentiment_label = "Very Positive"
        elif sentiment_score > 0.1:
            sentiment_label = "Positive"
        elif sentiment_score > -0.1:
            sentiment_label = "Neutral"
        elif sentiment_score > -0.3:
            sentiment_label = "Negative"
        else:
            sentiment_label = "Very Negative"
        
        return {
            "symbol": symbol,
            "sentiment_score": round(sentiment_score, 2),
            "sentiment_label": sentiment_label,
            "news_count": total,
            "positive_news": positive_count,
            "negative_news": negative_count,
            "neutral_news": neutral_count,
            "top_headlines": [n["title"] for n in news_items[:3]],
            "recommendation": self._get_recommendation(sentiment_score)
        }
    
    def _get_simulated_news(self, symbol: str) -> list:
        """Get simulated news (replace with real API in production)."""
        return [
            {"title": f"{symbol} reports strong quarterly earnings", "sentiment": "positive"},
            {"title": f"Analysts upgrade {symbol} stock", "sentiment": "positive"},
            {"title": f"{symbol} faces competition in market", "sentiment": "negative"},
            {"title": f"{symbol} announces new product launch", "sentiment": "positive"},
            {"title": f"Market uncertainty affects {symbol}", "sentiment": "neutral"}
        ]
    
    def _get_recommendation(self, score: float) -> str:
        """Get recommendation based on sentiment."""
        if score > 0.3:
            return "Strong positive sentiment - Consider buying"
        elif score > 0.1:
            return "Positive sentiment - Hold or accumulate"
        elif score > -0.1:
            return "Neutral sentiment - Hold current position"
        elif score > -0.3:
            return "Negative sentiment - Consider reducing"
        else:
            return "Very negative sentiment - Consider selling"


class TechnicalAgent:
    """Agent that analyzes technical indicators."""
    
    def __init__(self):
        self.name = "Technical Analyst"
    
    def analyze_technical(self, symbol: str) -> dict:
        """Perform technical analysis on a stock."""
        
        stock = yf.Ticker(symbol)
        hist = stock.history(period="6mo")
        
        if hist.empty:
            return {"error": "No data available"}
        
        # Calculate technical indicators
        rsi = self._calculate_rsi(hist['Close'])
        macd = self._calculate_macd(hist['Close'])
        sma_20 = hist['Close'].rolling(window=20).mean().iloc[-1]
        sma_50 = hist['Close'].rolling(window=50).mean().iloc[-1]
        current_price = hist['Close'].iloc[-1]
        
        # Determine trends
        price_vs_sma20 = "Above" if current_price > sma_20 else "Below"
        price_vs_sma50 = "Above" if current_price > sma_50 else "Below"
        sma_trend = "Bullish" if sma_20 > sma_50 else "Bearish"
        
        # RSI interpretation
        rsi_signal = self._interpret_rsi(rsi)
        
        # MACD signal
        macd_signal = "Bullish" if macd["macd"] > macd["signal"] else "Bearish"
        
        # Overall technical rating
        bullish_signals = sum([
            price_vs_sma20 == "Above",
            price_vs_sma50 == "Above",
            sma_trend == "Bullish",
            rsi_signal == "Oversold" or rsi_signal == "Neutral",
            macd_signal == "Bullish"
        ])
        
        if bullish_signals >= 4:
            overall_rating = "Strong Buy"
        elif bullish_signals >= 3:
            overall_rating = "Buy"
        elif bullish_signals >= 2:
            overall_rating = "Hold"
        elif bullish_signals >= 1:
            overall_rating = "Sell"
        else:
            overall_rating = "Strong Sell"
        
        return {
            "symbol": symbol,
            "current_price": round(current_price, 2),
            "rsi": round(rsi, 2),
            "rsi_signal": rsi_signal,
            "macd": round(macd["macd"], 2),
            "macd_signal": macd_signal,
            "sma_20": round(sma_20, 2),
            "sma_50": round(sma_50, 2),
            "price_vs_sma20": price_vs_sma20,
            "price_vs_sma50": price_vs_sma50,
            "sma_trend": sma_trend,
            "overall_rating": overall_rating,
            "support_level": round(hist['Low'].tail(20).min(), 2),
            "resistance_level": round(hist['High'].tail(20).max(), 2)
        }
    
    def _calculate_rsi(self, prices, period=14):
        """Calculate RSI indicator."""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi.iloc[-1]
    
    def _calculate_macd(self, prices):
        """Calculate MACD indicator."""
        exp1 = prices.ewm(span=12, adjust=False).mean()
        exp2 = prices.ewm(span=26, adjust=False).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=9, adjust=False).mean()
        return {
            "macd": macd.iloc[-1],
            "signal": signal.iloc[-1]
        }
    
    def _interpret_rsi(self, rsi):
        """Interpret RSI value."""
        if rsi > 70:
            return "Overbought"
        elif rsi < 30:
            return "Oversold"
        else:
            return "Neutral"


class TaxAgent:
    """Agent that suggests tax-loss harvesting opportunities."""
    
    def __init__(self):
        self.name = "Tax Advisor"
    
    def analyze_tax_opportunities(self, holdings: list) -> dict:
        """Analyze tax-loss harvesting opportunities."""
        
        opportunities = []
        total_potential_savings = 0
        
        for holding in holdings:
            symbol = holding["symbol"]
            shares = holding["shares"]
            current_price = holding.get("current_price", 0)
            avg_cost = holding.get("avg_cost", current_price)
            
            if current_price == 0:
                continue
            
            # Calculate gain/loss
            gain_per_share = current_price - avg_cost
            total_gain_loss = gain_per_share * shares
            
            # Tax loss harvesting opportunity
            if total_gain_loss < 0:
                potential_savings = abs(total_gain_loss) * 0.22
                opportunities.append({
                    "symbol": symbol,
                    "shares": shares,
                    "avg_cost": avg_cost,
                    "current_price": current_price,
                    "unrealized_loss": round(total_gain_loss, 2),
                    "potential_tax_savings": round(potential_savings, 2),
                    "recommendation": "Consider selling to harvest tax loss"
                })
                total_potential_savings += potential_savings
            
            elif total_gain_loss > 0:
                opportunities.append({
                    "symbol": symbol,
                    "shares": shares,
                    "avg_cost": avg_cost,
                    "current_price": current_price,
                    "unrealized_gain": round(total_gain_loss, 2),
                    "potential_tax_liability": round(total_gain_loss * 0.15, 2),
                    "recommendation": "Hold for long-term capital gains rate"
                })
        
        return {
            "opportunities": opportunities,
            "total_potential_savings": round(total_potential_savings, 2),
            "tax_brassack_assumption": "22%",
            "recommendation": self._get_tax_recommendation(opportunities)
        }
    
    def _get_tax_recommendation(self, opportunities: list) -> str:
        """Get tax recommendation."""
        losses = [o for o in opportunities if "unrealized_loss" in o]
        gains = [o for o in opportunities if "unrealized_gain" in o]
        
        if losses and gains:
            return "Consider harvesting losses to offset gains"
        elif losses:
            return "You have tax-loss harvesting opportunities"
        elif gains:
            return "Consider holding for long-term capital gains rate"
        else:
            return "No immediate tax actions needed"


class AlertAgent:
    """Agent that monitors price alerts."""
    
    def __init__(self, alerts_file="data/alerts.json"):
        self.alerts_file = alerts_file
        self.alerts = self._load_alerts()
    
    def _load_alerts(self) -> list:
        """Load alerts from file."""
        if os.path.exists(self.alerts_file):
            with open(self.alerts_file, 'r') as f:
                return json.load(f)
        return []
    
    def _save_alerts(self):
        """Save alerts to file."""
        os.makedirs(os.path.dirname(self.alerts_file), exist_ok=True)
        with open(self.alerts_file, 'w') as f:
            json.dump(self.alerts, f, indent=2)
    
    def add_alert(self, symbol: str, alert_type: str, target_price: float) -> dict:
        """Add a new price alert."""
        
        alert = {
            "id": len(self.alerts) + 1,
            "symbol": symbol.upper(),
            "alert_type": alert_type,  # "above" or "below"
            "target_price": target_price,
            "created_at": datetime.now().isoformat(),
            "triggered": False
        }
        
        self.alerts.append(alert)
        self._save_alerts()
        
        return {
            "status": "added",
            "alert": alert
        }
    
    def remove_alert(self, alert_id: int) -> dict:
        """Remove an alert."""
        self.alerts = [a for a in self.alerts if a["id"] != alert_id]
        self._save_alerts()
        return {"status": "removed"}
    
    def check_alerts(self) -> list:
        """Check if any alerts should be triggered."""
        
        triggered = []
        
        for alert in self.alerts:
            if alert["triggered"]:
                continue
            
            symbol = alert["symbol"]
            target_price = alert["target_price"]
            alert_type = alert["alert_type"]
            
            # Get current price
            stock = yf.Ticker(symbol)
            info = stock.info
            current_price = info.get("currentPrice", 0)
            
            if current_price == 0:
                continue
            
            # Check if alert should trigger
            if alert_type == "above" and current_price >= target_price:
                alert["triggered"] = True
                triggered.append({
                    "symbol": symbol,
                    "alert_type": alert_type,
                    "target_price": target_price,
                    "current_price": current_price,
                    "message": f"{symbol} is now above ${target_price} (Current: ${current_price})"
                })
            
            elif alert_type == "below" and current_price <= target_price:
                alert["triggered"] = True
                triggered.append({
                    "symbol": symbol,
                    "alert_type": alert_type,
                    "target_price": target_price,
                    "current_price": current_price,
                    "message": f"{symbol} is now below ${target_price} (Current: ${current_price})"
                })
        
        self._save_alerts()
        return triggered
    
    def get_active_alerts(self) -> list:
        """Get all active (non-triggered) alerts."""
        return [a for a in self.alerts if not a["triggered"]]
    
    def get_triggered_alerts(self) -> list:
        """Get all triggered alerts."""
        return [a for a in self.alerts if a["triggered"]]


class CompareAgent:
    """Agent that compares multiple stocks side-by-side."""
    
    def __init__(self):
        self.name = "Stock Comparator"
    
    def compare_stocks(self, symbols: list) -> dict:
        """Compare multiple stocks side-by-side."""
        
        comparisons = []
        
        for symbol in symbols:
            stock = yf.Ticker(symbol)
            info = stock.info
            hist = stock.history(period="1y")
            
            if hist.empty:
                continue
            
            # Get key metrics
            current_price = info.get("currentPrice", 0)
            market_cap = info.get("marketCap", 0)
            pe_ratio = info.get("trailingPE", 0)
            forward_pe = info.get("forwardPE", 0)
            dividend_yield = info.get("dividendYield", 0)
            beta = info.get("beta", 0)
            profit_margin = info.get("profitMargins", 0)
            revenue_growth = info.get("revenueGrowth", 0)
            debt_to_equity = info.get("debtToEquity", 0)
            roe = info.get("returnOnEquity", 0)
            
            # Calculate returns
            if len(hist) >= 252:
                year_return = ((hist['Close'].iloc[-1] / hist['Close'].iloc[-252]) - 1) * 100
            else:
                year_return = 0
            
            if len(hist) >= 63:
                quarter_return = ((hist['Close'].iloc[-1] / hist['Close'].iloc[-63]) - 1) * 100
            else:
                quarter_return = 0
            
            # Volatility
            volatility = hist['Close'].pct_change().std() * (252 ** 0.5) * 100
            
            # Price vs 52-week range
            high_52w = hist['High'].max()
            low_52w = hist['Low'].min()
            price_vs_52w = ((current_price - low_52w) / (high_52w - low_52w)) * 100 if high_52w != low_52w else 50
            
            comparisons.append({
                "symbol": symbol,
                "name": info.get("shortName", symbol),
                "sector": info.get("sector", "N/A"),
                "industry": info.get("industry", "N/A"),
                "current_price": round(current_price, 2),
                "market_cap": market_cap,
                "market_capformatted": self._format_large_number(market_cap),
                "pe_ratio": round(pe_ratio, 2) if pe_ratio else "N/A",
                "forward_pe": round(forward_pe, 2) if forward_pe else "N/A",
                "dividend_yield": round(dividend_yield * 100, 2) if dividend_yield else 0,
                "beta": round(beta, 2) if beta else "N/A",
                "profit_margin": round(profit_margin * 100, 2) if profit_margin else "N/A",
                "revenue_growth": round(revenue_growth * 100, 2) if revenue_growth else "N/A",
                "debt_to_equity": round(debt_to_equity, 2) if debt_to_equity else "N/A",
                "roe": round(roe * 100, 2) if roe else "N/A",
                "year_return": round(year_return, 2),
                "quarter_return": round(quarter_return, 2),
                "volatility": round(volatility, 2),
                "price_vs_52w": round(price_vs_52w, 2),
                "high_52w": round(high_52w, 2),
                "low_52w": round(low_52w, 2)
            })
        
        # Determine winner for each category
        winners = self._determine_winners(comparisons)
        
        # Overall recommendation
        recommendation = self._get_recommendation(comparisons, winners)
        
        return {
            "stocks": comparisons,
            "winners": winners,
            "recommendation": recommendation,
            "comparison_count": len(comparisons)
        }
    
    def _format_large_number(self, num: float) -> str:
        """Format large numbers (market cap)."""
        if num >= 1e12:
            return f"${num/1e12:.2f}T"
        elif num >= 1e9:
            return f"${num/1e9:.2f}B"
        elif num >= 1e6:
            return f"${num/1e6:.2f}M"
        else:
            return f"${num:,.2f}"
    
    def _determine_winners(self, comparisons: list) -> dict:
        """Determine which stock wins in each category."""
        
        if len(comparisons) < 2:
            return {}
        
        winners = {}
        
        # Best Value (lowest P/E)
        pe_stocks = [s for s in comparisons if isinstance(s["pe_ratio"], (int, float))]
        if pe_stocks:
            winners["best_value"] = min(pe_stocks, key=lambda x: x["pe_ratio"])["symbol"]
        
        # Best Growth (highest revenue growth)
        growth_stocks = [s for s in comparisons if isinstance(s["revenue_growth"], (int, float))]
        if growth_stocks:
            winners["best_growth"] = max(growth_stocks, key=lambda x: x["revenue_growth"])["symbol"]
        
        # Best Return (1 year)
        winners["best_return"] = max(comparisons, key=lambda x: x["year_return"])["symbol"]
        
        # Lowest Risk (lowest volatility)
        winners["lowest_risk"] = min(comparisons, key=lambda x: x["volatility"])["symbol"]
        
        # Best Dividend
        div_stocks = [s for s in comparisons if s["dividend_yield"] > 0]
        if div_stocks:
            winners["best_dividend"] = max(div_stocks, key=lambda x: x["dividend_yield"])["symbol"]
        
        # Most Profitable (highest profit margin)
        margin_stocks = [s for s in comparisons if isinstance(s["profit_margin"], (int, float))]
        if margin_stocks:
            winners["most_profitable"] = max(margin_stocks, key=lambda x: x["profit_margin"])["symbol"]
        
        # Best ROE
        roe_stocks = [s for s in comparisons if isinstance(s["roe"], (int, float))]
        if roe_stocks:
            winners["best_roe"] = max(roe_stocks, key=lambda x: x["roe"])["symbol"]
        
        return winners
    
    def _get_recommendation(self, comparisons: list, winners: dict) -> str:
        """Get overall recommendation based on comparison."""
        
        if len(comparisons) < 2:
            return "Need at least 2 stocks to compare."
        
        # Count wins
        win_count = {}
        for category, symbol in winners.items():
            win_count[symbol] = win_count.get(symbol, 0) + 1
        
        # Get overall winner
        overall_winner = max(win_count, key=win_count.get)
        winner_name = next(s["name"] for s in comparisons if s["symbol"] == overall_winner)
        
        # Build recommendation
        rec = f"**Overall Winner: {overall_winner} ({winner_name})**\n\n"
        rec += f"It wins in {win_count[overall_winner]} out of {len(winners)} categories.\n\n"
        
        # Category winners
        rec += "**Category Winners:**\n"
        category_names = {
            "best_value": "Best Value (Low P/E)",
            "best_growth": "Best Growth",
            "best_return": "Best 1-Year Return",
            "lowest_risk": "Lowest Risk",
            "best_dividend": "Best Dividend",
            "most_profitable": "Most Profitable",
            "best_roe": "Best ROE"
        }
        
        for category, symbol in winners.items():
            rec += f"- {category_names.get(category, category)}: {symbol}\n"
        
        return rec
