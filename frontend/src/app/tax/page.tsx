'use client';

import { useState } from 'react';
import { api } from '@/lib/api';
import { DollarSign, TrendingDown, AlertCircle } from 'lucide-react';

interface TaxOpportunity {
  symbol: string;
  shares: number;
  avg_cost: number;
  current_price: number;
  unrealized_loss?: number;
  unrealized_gain?: number;
  potential_tax_savings?: number;
  potential_tax_liability?: number;
  recommendation: string;
}

interface TaxResult {
  opportunities: TaxOpportunity[];
  total_potential_savings: number;
  tax_brassack_assumption: string;
  recommendation: string;
}

export default function TaxPage() {
  const [result, setResult] = useState<TaxResult | null>(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    setLoading(true);
    try {
      const portfolio = await api.getPortfolio();
      const data = await fetch('/api/tax/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(portfolio.holdings),
      }).then(r => r.json());
      setResult(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-3xl font-bold">Tax Optimization</h1>
        <p className="text-gray-400 mt-1">Find tax-loss harvesting opportunities</p>
      </div>

      <button
        onClick={handleAnalyze}
        disabled={loading}
        className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 disabled:cursor-not-allowed rounded-xl px-6 py-3 font-medium transition-colors"
      >
        {loading ? 'Analyzing...' : 'Analyze Tax Opportunities'}
      </button>

      {result && (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
              <p className="text-sm text-gray-400">Potential Tax Savings</p>
              <p className="text-2xl font-bold mt-1 text-green-400">${result.total_potential_savings.toLocaleString()}</p>
            </div>
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
              <p className="text-sm text-gray-400">Tax Bracket Assumption</p>
              <p className="text-2xl font-bold mt-1">{result.tax_brassack_assumption}</p>
            </div>
          </div>

          {/* Opportunities */}
          <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
            <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <DollarSign size={20} className="text-green-400" />
              Tax Opportunities
            </h2>
            <div className="space-y-4">
              {result.opportunities.map((opp) => (
                <div key={opp.symbol} className="bg-gray-800 rounded-xl p-4">
                  <div className="flex justify-between items-start mb-3">
                    <div>
                      <h3 className="font-semibold text-lg">{opp.symbol}</h3>
                      <p className="text-sm text-gray-400">{opp.shares} shares @ ${opp.avg_cost.toFixed(2)}</p>
                    </div>
                    {opp.unrealized_loss !== undefined && (
                      <div className="bg-green-500/10 px-3 py-1 rounded-lg">
                        <p className="text-green-400 font-semibold">-${Math.abs(opp.unrealized_loss).toLocaleString()}</p>
                        <p className="text-xs text-gray-400">Potential savings: ${opp.potential_tax_savings?.toLocaleString()}</p>
                      </div>
                    )}
                    {opp.unrealized_gain !== undefined && (
                      <div className="bg-yellow-500/10 px-3 py-1 rounded-lg">
                        <p className="text-yellow-400 font-semibold">+${opp.unrealized_gain.toLocaleString()}</p>
                        <p className="text-xs text-gray-400">Tax liability: ${opp.potential_tax_liability?.toLocaleString()}</p>
                      </div>
                    )}
                  </div>
                  <div className="flex items-start gap-2 p-3 bg-gray-700/50 rounded-lg">
                    <AlertCircle size={16} className="text-blue-400 mt-0.5 flex-shrink-0" />
                    <p className="text-sm text-gray-300">{opp.recommendation}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-gradient-to-r from-green-600/20 to-emerald-600/20 border border-green-500/20 rounded-xl p-6">
            <h2 className="text-lg font-semibold mb-3">Overall Recommendation</h2>
            <p className="text-gray-300">{result.recommendation}</p>
          </div>
        </>
      )}
    </div>
  );
}
