'use client';

import { useState, useEffect } from 'react';
import { api, PortfolioSummary } from '@/lib/api';
import { Plus, Trash2, RefreshCw } from 'lucide-react';

export default function HoldingsPage() {
  const [portfolio, setPortfolio] = useState<PortfolioSummary | null>(null);
  const [symbol, setSymbol] = useState('');
  const [shares, setShares] = useState('');
  const [avgCost, setAvgCost] = useState('');
  const [loading, setLoading] = useState(true);

  const fetchPortfolio = async () => {
    setLoading(true);
    try {
      const data = await api.getPortfolio();
      setPortfolio(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPortfolio();
  }, []);

  const handleAdd = async () => {
    if (!symbol || !shares || !avgCost) return;
    try {
      await api.addHolding(symbol.toUpperCase(), parseFloat(shares), parseFloat(avgCost));
      setSymbol('');
      setShares('');
      setAvgCost('');
      fetchPortfolio();
    } catch (err) {
      console.error(err);
    }
  };

  const handleRemove = async (sym: string) => {
    try {
      await api.removeHolding(sym);
      fetchPortfolio();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Manage Holdings</h1>
          <p className="text-gray-400 mt-1">Add or remove stocks from your portfolio</p>
        </div>
        <button
          onClick={fetchPortfolio}
          className="bg-gray-800 hover:bg-gray-700 p-3 rounded-lg transition-colors"
        >
          <RefreshCw size={20} />
        </button>
      </div>

      {/* Add Holding Form */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
        <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
          <Plus size={20} className="text-blue-400" />
          Add New Holding
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <input
            type="text"
            value={symbol}
            onChange={(e) => setSymbol(e.target.value.toUpperCase())}
            placeholder="Symbol (e.g., AAPL)"
            className="bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500"
          />
          <input
            type="number"
            value={shares}
            onChange={(e) => setShares(e.target.value)}
            placeholder="Shares"
            className="bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500"
          />
          <input
            type="number"
            value={avgCost}
            onChange={(e) => setAvgCost(e.target.value)}
            placeholder="Avg Cost ($)"
            className="bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500"
          />
          <button
            onClick={handleAdd}
            disabled={!symbol || !shares || !avgCost}
            className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 disabled:cursor-not-allowed rounded-lg px-4 py-3 font-medium transition-colors"
          >
            Add Holding
          </button>
        </div>
      </div>

      {/* Holdings List */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
        <h2 className="text-lg font-semibold mb-4">Current Holdings</h2>
        {loading ? (
          <div className="text-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto"></div>
          </div>
        ) : portfolio && portfolio.holdings.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="text-left text-sm text-gray-400 border-b border-gray-800">
                  <th className="pb-3">Symbol</th>
                  <th className="pb-3">Shares</th>
                  <th className="pb-3">Current Price</th>
                  <th className="pb-3">Value</th>
                  <th className="pb-3"></th>
                </tr>
              </thead>
              <tbody>
              {portfolio.holdings.map((h) => (
                <tr key={h.symbol} className="border-b border-gray-800/50 hover:bg-gray-800/30">
                  <td className="py-4 font-semibold">{h.symbol}</td>
                  <td className="py-4 text-gray-300">{h.shares}</td>
                  <td className="py-4 text-gray-300">${h.current_price.toFixed(2)}</td>
                  <td className="py-4 text-gray-300">${h.value.toLocaleString()}</td>
                  <td className="py-4">
                    <button
                      onClick={() => handleRemove(h.symbol)}
                      className="text-red-400 hover:text-red-300 p-2"
                    >
                      <Trash2 size={18} />
                    </button>
                  </td>
                </tr>
              ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p className="text-gray-500 text-center py-8">No holdings yet. Add your first stock above.</p>
        )}
      </div>
    </div>
  );
}
