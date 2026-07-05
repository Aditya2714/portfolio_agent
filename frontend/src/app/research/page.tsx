'use client';

import { useState } from 'react';
import { api, StockInfo, TechnicalResult } from '@/lib/api';
import { Search, TrendingUp, TrendingDown, Activity, BarChart3 } from 'lucide-react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from 'recharts';

export default function ResearchPage() {
  const [symbol, setSymbol] = useState('');
  const [stockInfo, setStockInfo] = useState<StockInfo | null>(null);
  const [technical, setTechnical] = useState<TechnicalResult | null>(null);
  const [history, setHistory] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSearch = async () => {
    if (!symbol.trim()) return;
    setLoading(true);
    setError('');
    setStockInfo(null);
    setTechnical(null);

    try {
      const [info, tech, hist] = await Promise.all([
        api.getStockInfo(symbol),
        api.getTechnical(symbol),
        api.getStockHistory(symbol),
      ]);
      setStockInfo(info);
      setTechnical(tech);
      setHistory((hist as any).history || []);
    } catch (err) {
      setError('Could not fetch stock data. Check the symbol and try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-3xl font-bold">Stock Research</h1>
        <p className="text-gray-400 mt-1">Analyze individual stocks</p>
      </div>

      {/* Search */}
      <div className="flex gap-3">
        <div className="flex-1 relative">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500" size={20} />
          <input
            type="text"
            value={symbol}
            onChange={(e) => setSymbol(e.target.value.toUpperCase())}
            onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
            placeholder="Enter stock symbol (e.g., AAPL)"
            className="w-full bg-gray-900 border border-gray-700 rounded-xl pl-12 pr-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500"
          />
        </div>
        <button
          onClick={handleSearch}
          disabled={loading || !symbol.trim()}
          className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 disabled:cursor-not-allowed rounded-xl px-6 py-3 font-medium transition-colors"
        >
          {loading ? 'Loading...' : 'Research'}
        </button>
      </div>

      {error && (
        <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-4 text-red-400">
          {error}
        </div>
      )}

      {stockInfo && technical && (
        <>
          {/* Key Metrics */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
              <p className="text-sm text-gray-400">Current Price</p>
              <p className="text-2xl font-bold mt-1">${stockInfo.current_price.toFixed(2)}</p>
            </div>
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
              <p className="text-sm text-gray-400">Market Cap</p>
              <p className="text-2xl font-bold mt-1">${(stockInfo.market_cap / 1e9).toFixed(2)}B</p>
            </div>
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
              <p className="text-sm text-gray-400">P/E Ratio</p>
              <p className="text-2xl font-bold mt-1">{stockInfo.pe_ratio?.toFixed(2) || 'N/A'}</p>
            </div>
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
              <p className="text-sm text-gray-400">52W High</p>
              <p className="text-2xl font-bold mt-1">${stockInfo.week52_high?.toFixed(2) || 'N/A'}</p>
            </div>
          </div>

          {/* Technical Indicators */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
              <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <Activity size={20} className="text-blue-400" />
                Technical Indicators
              </h2>
              <div className="space-y-4">
                <div className="flex justify-between items-center p-3 bg-gray-800 rounded-lg">
                  <span className="text-gray-400">RSI (14)</span>
                  <div className="text-right">
                    <span className="font-semibold">{technical.rsi?.toFixed(2)}</span>
                    <span className={`ml-2 text-xs px-2 py-0.5 rounded ${
                      technical.rsi_signal === 'Oversold' ? 'bg-green-500/20 text-green-400' :
                      technical.rsi_signal === 'Overbought' ? 'bg-red-500/20 text-red-400' :
                      'bg-gray-500/20 text-gray-400'
                    }`}>
                      {technical.rsi_signal}
                    </span>
                  </div>
                </div>
                <div className="flex justify-between items-center p-3 bg-gray-800 rounded-lg">
                  <span className="text-gray-400">MACD</span>
                  <div className="text-right">
                    <span className="font-semibold">{technical.macd?.toFixed(2)}</span>
                    <span className={`ml-2 text-xs px-2 py-0.5 rounded ${
                      technical.macd_signal === 'Bullish' ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'
                    }`}>
                      {technical.macd_signal}
                    </span>
                  </div>
                </div>
                <div className="flex justify-between items-center p-3 bg-gray-800 rounded-lg">
                  <span className="text-gray-400">SMA 20</span>
                  <span className="font-semibold">${technical.sma_20?.toFixed(2)}</span>
                </div>
                <div className="flex justify-between items-center p-3 bg-gray-800 rounded-lg">
                  <span className="text-gray-400">SMA 50</span>
                  <span className="font-semibold">${technical.sma_50?.toFixed(2)}</span>
                </div>
                <div className="flex justify-between items-center p-3 bg-gray-800 rounded-lg">
                  <span className="text-gray-400">Trend</span>
                  <span className={`font-semibold ${
                    technical.sma_trend === 'Bullish' ? 'text-green-400' : 'text-red-400'
                  }`}>
                    {technical.sma_trend}
                  </span>
                </div>
              </div>
            </div>

            <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
              <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <BarChart3 size={20} className="text-purple-400" />
                Rating & Levels
              </h2>
              <div className="text-center py-6">
                <div className={`inline-block px-6 py-3 rounded-xl text-xl font-bold ${
                  technical.overall_rating?.includes('Buy') ? 'bg-green-500/20 text-green-400' :
                  technical.overall_rating?.includes('Sell') ? 'bg-red-500/20 text-red-400' :
                  'bg-yellow-500/20 text-yellow-400'
                }`}>
                  {technical.overall_rating}
                </div>
              </div>
              <div className="space-y-3 mt-4">
                <div className="flex justify-between p-3 bg-gray-800 rounded-lg">
                  <span className="text-gray-400">Support Level</span>
                  <span className="font-semibold text-green-400">${technical.support_level?.toFixed(2)}</span>
                </div>
                <div className="flex justify-between p-3 bg-gray-800 rounded-lg">
                  <span className="text-gray-400">Resistance Level</span>
                  <span className="font-semibold text-red-400">${technical.resistance_level?.toFixed(2)}</span>
                </div>
              </div>
            </div>
          </div>

          {/* Company Info */}
          <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
            <h2 className="text-lg font-semibold mb-4">Company Info</h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div>
                <p className="text-sm text-gray-400">Name</p>
                <p className="font-medium">{stockInfo.name}</p>
              </div>
              <div>
                <p className="text-sm text-gray-400">Sector</p>
                <p className="font-medium">{stockInfo.sector}</p>
              </div>
              <div>
                <p className="text-sm text-gray-400">Industry</p>
                <p className="font-medium">{stockInfo.industry}</p>
              </div>
              <div>
                <p className="text-sm text-gray-400">Dividend Yield</p>
                <p className="font-medium">{(stockInfo.dividend_yield * 100).toFixed(2)}%</p>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
