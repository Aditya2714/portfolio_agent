'use client';

import { useState, useEffect } from 'react';
import { api, TechnicalResult, PortfolioSummary } from '@/lib/api';
import { Activity, TrendingUp, TrendingDown, ArrowUp, ArrowDown } from 'lucide-react';

export default function TechnicalPage() {
  const [portfolio, setPortfolio] = useState<PortfolioSummary | null>(null);
  const [selectedSymbol, setSelectedSymbol] = useState('');
  const [result, setResult] = useState<TechnicalResult | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    api.getPortfolio().then(setPortfolio).catch(console.error);
  }, []);

  const handleAnalyze = async () => {
    if (!selectedSymbol) return;
    setLoading(true);
    try {
      const data = await api.getTechnical(selectedSymbol);
      setResult(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getRatingColor = (rating: string) => {
    if (rating.includes('Buy')) return 'bg-green-500/20 text-green-400 border-green-500/30';
    if (rating.includes('Sell')) return 'bg-red-500/20 text-red-400 border-red-500/30';
    return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30';
  };

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-3xl font-bold">Technical Analysis</h1>
        <p className="text-gray-400 mt-1">Analyze technical indicators for your stocks</p>
      </div>

      {/* Stock Selection */}
      <div className="flex gap-3">
        <select
          value={selectedSymbol}
          onChange={(e) => setSelectedSymbol(e.target.value)}
          className="flex-1 bg-gray-900 border border-gray-700 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-blue-500"
        >
          <option value="">Select a stock</option>
          {portfolio?.holdings.map((h) => (
            <option key={h.symbol} value={h.symbol}>{h.symbol}</option>
          ))}
        </select>
        <button
          onClick={handleAnalyze}
          disabled={loading || !selectedSymbol}
          className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 disabled:cursor-not-allowed rounded-xl px-6 py-3 font-medium transition-colors"
        >
          {loading ? 'Analyzing...' : 'Analyze'}
        </button>
      </div>

      {result && (
        <>
          {/* Key Metrics */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
              <p className="text-sm text-gray-400">Current Price</p>
              <p className="text-2xl font-bold mt-1">${result.current_price?.toFixed(2)}</p>
            </div>
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
              <p className="text-sm text-gray-400">RSI (14)</p>
              <p className="text-2xl font-bold mt-1">{result.rsi?.toFixed(2)}</p>
              <p className={`text-xs mt-1 ${
                result.rsi > 70 ? 'text-red-400' : result.rsi < 30 ? 'text-green-400' : 'text-gray-400'
              }`}>
                {result.rsi_signal}
              </p>
            </div>
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
              <p className="text-sm text-gray-400">MACD</p>
              <p className="text-2xl font-bold mt-1">{result.macd?.toFixed(2)}</p>
              <p className={`text-xs mt-1 ${
                result.macd_signal === 'Bullish' ? 'text-green-400' : 'text-red-400'
              }`}>
                {result.macd_signal}
              </p>
            </div>
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
              <p className="text-sm text-gray-400">Overall Rating</p>
              <div className={`inline-block px-3 py-1 rounded-lg text-sm font-semibold border mt-2 ${getRatingColor(result.overall_rating)}`}>
                {result.overall_rating}
              </div>
            </div>
          </div>

          {/* Moving Averages & Signals */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
              <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <Activity size={20} className="text-blue-400" />
                Moving Averages
              </h2>
              <div className="space-y-3">
                <div className="flex justify-between items-center p-3 bg-gray-800 rounded-lg">
                  <span className="text-gray-400">SMA 20</span>
                  <div className="text-right">
                    <span className="font-semibold">${result.sma_20?.toFixed(2)}</span>
                    <span className={`ml-2 text-xs ${result.price_vs_sma20 === 'Above' ? 'text-green-400' : 'text-red-400'}`}>
                      {result.price_vs_sma20 === 'Above' ? '↑' : '↓'} Price {result.price_vs_sma20}
                    </span>
                  </div>
                </div>
                <div className="flex justify-between items-center p-3 bg-gray-800 rounded-lg">
                  <span className="text-gray-400">SMA 50</span>
                  <div className="text-right">
                    <span className="font-semibold">${result.sma_50?.toFixed(2)}</span>
                    <span className={`ml-2 text-xs ${result.price_vs_sma50 === 'Above' ? 'text-green-400' : 'text-red-400'}`}>
                      {result.price_vs_sma50 === 'Above' ? '↑' : '↓'} Price {result.price_vs_sma50}
                    </span>
                  </div>
                </div>
                <div className="flex justify-between items-center p-3 bg-gray-800 rounded-lg">
                  <span className="text-gray-400">SMA Trend</span>
                  <span className={`font-semibold ${
                    result.sma_trend === 'Bullish' ? 'text-green-400' : 'text-red-400'
                  }`}>
                    {result.sma_trend === 'Bullish' ? '📈' : '📉'} {result.sma_trend}
                  </span>
                </div>
              </div>
            </div>

            <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
              <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <TrendingUp size={20} className="text-purple-400" />
                Support & Resistance
              </h2>
              <div className="space-y-3">
                <div className="p-4 bg-green-500/10 border border-green-500/20 rounded-lg">
                  <p className="text-sm text-green-400 mb-1">Support Level</p>
                  <p className="text-2xl font-bold text-green-400">${result.support_level?.toFixed(2)}</p>
                  <p className="text-xs text-gray-400 mt-1">Price floor - good buying zone</p>
                </div>
                <div className="p-4 bg-red-500/10 border border-red-500/20 rounded-lg">
                  <p className="text-sm text-red-400 mb-1">Resistance Level</p>
                  <p className="text-2xl font-bold text-red-400">${result.resistance_level?.toFixed(2)}</p>
                  <p className="text-xs text-gray-400 mt-1">Price ceiling - may face selling pressure</p>
                </div>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
