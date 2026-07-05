'use client';

import { useState } from 'react';
import { api, CompareResult } from '@/lib/api';
import { GitCompare, Trophy, TrendingUp, Shield, DollarSign, BarChart3 } from 'lucide-react';

export default function ComparePage() {
  const [input, setInput] = useState('');
  const [result, setResult] = useState<CompareResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleCompare = async () => {
    if (!input.trim()) return;
    const symbols = input.split(',').map(s => s.trim().toUpperCase()).filter(Boolean);
    if (symbols.length < 2) {
      setError('Please enter at least 2 stock symbols');
      return;
    }

    setLoading(true);
    setError('');
    try {
      const data = await api.compareStocks(symbols);
      setResult(data);
    } catch (err) {
      setError('Could not compare stocks. Check symbols and try again.');
    } finally {
      setLoading(false);
    }
  };

  const categoryLabels: Record<string, string> = {
    best_value: 'Best Value',
    best_growth: 'Best Growth',
    best_return: 'Best Return',
    lowest_risk: 'Lowest Risk',
    best_dividend: 'Best Dividend',
    most_profitable: 'Most Profitable',
    best_roe: 'Best ROE',
  };

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-3xl font-bold">Compare Stocks</h1>
        <p className="text-gray-400 mt-1">Compare multiple stocks side-by-side</p>
      </div>

      {/* Input */}
      <div className="flex gap-3">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleCompare()}
          placeholder="Enter symbols separated by commas (e.g., AAPL, MSFT, GOOGL)"
          className="flex-1 bg-gray-900 border border-gray-700 rounded-xl px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500"
        />
        <button
          onClick={handleCompare}
          disabled={loading || !input.trim()}
          className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 disabled:cursor-not-allowed rounded-xl px-6 py-3 font-medium transition-colors flex items-center gap-2"
        >
          <GitCompare size={18} />
          {loading ? 'Comparing...' : 'Compare'}
        </button>
      </div>

      {error && (
        <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-4 text-red-400">
          {error}
        </div>
      )}

      {result && (
        <>
          {/* Category Winners */}
          {Object.keys(result.winners).length > 0 && (
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
              <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <Trophy size={20} className="text-yellow-400" />
                Category Winners
              </h2>
              <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-3">
                {Object.entries(result.winners).map(([category, symbol]) => (
                  <div key={category} className="bg-gray-800 rounded-lg p-3 text-center">
                    <p className="text-xs text-gray-400">{categoryLabels[category]}</p>
                    <p className="text-lg font-bold text-blue-400 mt-1">{symbol}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Comparison Table */}
          <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
            <h2 className="text-lg font-semibold mb-4">Comparison</h2>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="text-left text-sm text-gray-400 border-b border-gray-800">
                    <th className="pb-3">Stock</th>
                    <th className="pb-3">Price</th>
                    <th className="pb-3">Market Cap</th>
                    <th className="pb-3">P/E Ratio</th>
                    <th className="pb-3">1Y Return</th>
                    <th className="pb-3">Volatility</th>
                    <th className="pb-3">Dividend</th>
                  </tr>
                </thead>
                <tbody>
                  {result.stocks.map((stock) => (
                    <tr key={stock.symbol} className="border-b border-gray-800/50 hover:bg-gray-800/30">
                      <td className="py-4">
                        <div>
                          <p className="font-semibold">{stock.symbol}</p>
                          <p className="text-xs text-gray-400">{stock.name}</p>
                        </div>
                      </td>
                      <td className="py-4 font-medium">${stock.current_price.toFixed(2)}</td>
                      <td className="py-4 text-gray-300">${(stock.market_cap / 1e9).toFixed(2)}B</td>
                      <td className="py-4 text-gray-300">{stock.pe_ratio?.toFixed(2) || 'N/A'}</td>
                      <td className={`py-4 font-medium ${stock.year_return >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                        {stock.year_return >= 0 ? '+' : ''}{stock.year_return.toFixed(2)}%
                      </td>
                      <td className="py-4 text-gray-300">{stock.volatility.toFixed(2)}%</td>
                      <td className="py-4 text-gray-300">{stock.dividend_yield.toFixed(2)}%</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Recommendation */}
          <div className="bg-gradient-to-r from-blue-600/20 to-cyan-600/20 border border-blue-500/20 rounded-xl p-6">
            <h2 className="text-lg font-semibold mb-3 flex items-center gap-2">
              <TrendingUp size={20} className="text-blue-400" />
              Recommendation
            </h2>
            <div className="text-gray-300 whitespace-pre-wrap">{result.recommendation}</div>
          </div>
        </>
      )}
    </div>
  );
}
