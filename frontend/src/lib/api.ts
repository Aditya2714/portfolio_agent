const API_BASE = '/api';

export interface PortfolioSummary {
  total_value: number;
  total_return_pct: number;
  holdings: Holding[];
  allocation: Record<string, number>;
  risk: {
    risk_level: string;
    risk_score: number;
  };
}

export interface Holding {
  symbol: string;
  shares: number;
  current_price: number;
  value: number;
}

export interface StockInfo {
  symbol: string;
  name: string;
  sector: string;
  industry: string;
  current_price: number;
  market_cap: number;
  pe_ratio: number;
  dividend_yield: number;
  week52_high: number;
  week52_low: number;
}

export interface CompareResult {
  stocks: StockComparison[];
  winners: Record<string, string>;
  recommendation: string;
}

export interface StockComparison {
  symbol: string;
  name: string;
  current_price: number;
  market_cap: number;
  pe_ratio: number;
  year_return: number;
  volatility: number;
  dividend_yield: number;
}

export interface SentimentResult {
  symbol: string;
  sentiment_score: number;
  sentiment_label: string;
  news_count: number;
  positive_news: number;
  negative_news: number;
  neutral_news: number;
  top_headlines: string[];
  recommendation: string;
}

export interface TechnicalResult {
  symbol: string;
  current_price: number;
  rsi: number;
  rsi_signal: string;
  macd: number;
  macd_signal: string;
  sma_20: number;
  sma_50: number;
  price_vs_sma20: string;
  price_vs_sma50: string;
  sma_trend: string;
  overall_rating: string;
  support_level: number;
  resistance_level: number;
}

class ApiClient {
  private async fetch<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const res = await fetch(`${API_BASE}${endpoint}`, {
      headers: { 'Content-Type': 'application/json' },
      ...options,
    });

    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(error.detail || `API error: ${res.status}`);
    }

    return res.json();
  }

  // Portfolio
  async getPortfolio(): Promise<PortfolioSummary> {
    return this.fetch<PortfolioSummary>('/portfolio');
  }

  async addHolding(symbol: string, shares: number, avgCost: number) {
    return this.fetch('/portfolio/holdings', {
      method: 'POST',
      body: JSON.stringify({ symbol, shares, avg_cost: avgCost }),
    });
  }

  async removeHolding(symbol: string) {
    return this.fetch(`/portfolio/holdings/${symbol}`, { method: 'DELETE' });
  }

  // Stock
  async getStockInfo(symbol: string): Promise<StockInfo> {
    return this.fetch<StockInfo>(`/stock/${symbol}`);
  }

  async getStockHistory(symbol: string, period: string = '1y') {
    return this.fetch(`/stock/${symbol}/history?period=${period}`);
  }

  // Compare
  async compareStocks(symbols: string[]): Promise<CompareResult> {
    return this.fetch<CompareResult>('/compare', {
      method: 'POST',
      body: JSON.stringify({ symbols }),
    });
  }

  // Sentiment
  async getSentiment(symbol: string): Promise<SentimentResult> {
    return this.fetch<SentimentResult>(`/sentiment/${symbol}`);
  }

  // Technical
  async getTechnical(symbol: string): Promise<TechnicalResult> {
    return this.fetch<TechnicalResult>(`/technical/${symbol}`);
  }

  // AI
  async askAI(query: string, portfolio?: PortfolioSummary) {
    return this.fetch('/ai/analyze', {
      method: 'POST',
      body: JSON.stringify({ query, portfolio }),
    });
  }
}

export const api = new ApiClient();
