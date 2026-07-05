'use client';

import { useState, useEffect } from 'react';
import { api, PortfolioSummary } from '@/lib/api';
import { FileText, Download, BarChart3, PieChart, TrendingUp, Shield } from 'lucide-react';
import {
  PieChart as RechartsPie,
  Pie,
  Cell,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip
} from 'recharts';

const COLORS = ['#0ea5e9', '#22c55e', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899'];

export default function ReportsPage() {
  const [portfolio, setPortfolio] = useState<PortfolioSummary | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getPortfolio()
      .then(setPortfolio)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (!portfolio) {
    return (
      <div className="text-center text-gray-400 mt-20">
        <p className="text-xl">No data available</p>
      </div>
    );
  }

  const allocationData = Object.entries(portfolio.allocation).map(([name, value]) => ({
    name,
    value: Number(value),
  }));

  const performanceData = portfolio.holdings.map(h => ({
    symbol: h.symbol,
    value: h.value,
  }));

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Portfolio Report</h1>
          <p className="text-gray-400 mt-1">Executive summary of your portfolio</p>
        </div>
      </div>

      {/* Executive Summary */}
      <div className="bg-gradient-to-r from-blue-600/20 to-cyan-600/20 border border-blue-500/20 rounded-xl p-6">
        <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
          <FileText size={20} className="text-blue-400" />
          Executive Summary
        </h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div>
            <p className="text-sm text-gray-400">Portfolio Value</p>
            <p className="text-2xl font-bold">${portfolio.total_value.toLocaleString()}</p>
          </div>
          <div>
            <p className="text-sm text-gray-400">Total Return</p>
            <p className={`text-2xl font-bold ${portfolio.total_return_pct >= 0 ? 'text-green-400' : 'text-red-400'}`}>
              {portfolio.total_return_pct}%
            </p>
          </div>
          <div>
            <p className="text-sm text-gray-400">Risk Level</p>
            <p className="text-2xl font-bold">{portfolio.risk?.risk_level || 'N/A'}</p>
          </div>
          <div>
            <p className="text-sm text-gray-400">Holdings</p>
            <p className="text-2xl font-bold">{portfolio.holdings.length}</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Allocation Chart */}
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
          <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <PieChart size={20} className="text-purple-400" />
            Asset Allocation
          </h2>
          <div className="h-64">
            <ResponsiveContainer>
              <RechartsPie>
                <Pie
                  data={allocationData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={100}
                  paddingAngle={2}
                  dataKey="value"
                  label={({ name, value }) => `${name}: ${value}%`}
                >
                  {allocationData.map((_, index) => (
                    <Cell key={index} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </RechartsPie>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Holdings Performance */}
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
          <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <BarChart3 size={20} className="text-green-400" />
            Holdings Performance
          </h2>
          <div className="h-64">
            <ResponsiveContainer>
              <BarChart data={performanceData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis dataKey="symbol" stroke="#6b7280" fontSize={12} />
                <YAxis stroke="#6b7280" fontSize={12} />
                <Tooltip
                  contentStyle={{ background: '#1f2937', border: '1px solid #374151' }}
                  formatter={(value: number) => [`$${value.toLocaleString()}`, 'Value']}
                />
                <Bar
                  dataKey="value"
                  fill="#0ea5e9"
                  radius={[4, 4, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Holdings Table */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
        <h2 className="text-lg font-semibold mb-4">Detailed Holdings</h2>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="text-left text-sm text-gray-400 border-b border-gray-800">
                <th className="pb-3">Symbol</th>
                <th className="pb-3">Shares</th>
                <th className="pb-3">Current Price</th>
                <th className="pb-3">Total Value</th>
              </tr>
            </thead>
            <tbody>
              {portfolio.holdings.map((h) => (
                <tr key={h.symbol} className="border-b border-gray-800/50 hover:bg-gray-800/30">
                  <td className="py-4 font-semibold">{h.symbol}</td>
                  <td className="py-4 text-gray-300">{h.shares}</td>
                  <td className="py-4 text-gray-300">${h.current_price.toFixed(2)}</td>
                  <td className="py-4 text-gray-300">${h.value.toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Risk Assessment */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
        <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
          <Shield size={20} className="text-yellow-400" />
          Risk Assessment
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-gray-800 rounded-lg p-4">
            <p className="text-sm text-gray-400">Risk Level</p>
            <p className="text-xl font-bold mt-1">{portfolio.risk?.risk_level || 'N/A'}</p>
          </div>
          <div className="bg-gray-800 rounded-lg p-4">
            <p className="text-sm text-gray-400">Risk Score</p>
            <p className="text-xl font-bold mt-1">{portfolio.risk?.risk_score || 'N/A'}/10</p>
          </div>
          <div className="bg-gray-800 rounded-lg p-4">
            <p className="text-sm text-gray-400">Diversification</p>
            <p className="text-xl font-bold mt-1">
              {portfolio.holdings.length >= 5 ? 'Good' : portfolio.holdings.length >= 3 ? 'Moderate' : 'Poor'}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
