'use client';

import { useState, useEffect } from 'react';
import { api, SentimentResult, PortfolioSummary } from '@/lib/api';
import { Newspaper, TrendingUp, TrendingDown, Minus, Search } from 'lucide-react';

export default function SentimentPage() {
  const [portfolio, setPortfolio] = useState<PortfolioSummary | null>(null);
  const [selectedSymbol, setSelectedSymbol] = useState('');
  const [result, setResult] = useState<SentimentResult | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    api.getPortfolio().then(setPortfolio).catch(console.error);
  }, []);

  const handleAnalyze = async () => {
    if (!selectedSymbol) return;
    setLoading(true);
    try {
      const data = await api.getSentiment(selectedSymbol);
      setResult(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getSentimentColor = (label: string) => {
    if (label.includes('Positive')) return 'text-green-400 bg-green-500/10';
    if (label.includes('Negative')) return 'text-red-400 bg-red-500/10';
    return 'text-yellow-400 bg-yellow-500/10';
  };

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-3xl font-bold">Sentiment Analysis</h1>
        <p className="text-gray-400 mt-1">Analyze news sentiment for your stocks</p>
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
          {/* Summary Cards */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
              <p className="text-sm text-gray-400">Sentiment Score</p>
              <p className="text-2xl font-bold mt-1">{result.sentiment_score}</p>
            </div>
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
              <p className="text-sm text-gray-400">Overall Sentiment</p>
              <p className={`text-lg font-bold mt-1 ${getSentimentColor(result.sentiment_label)}`}>
                {result.sentiment_label}
              </p>
            </div>
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
              <p className="text-sm text-gray-400">Total News</p>
              <p className="text-2xl font-bold mt-1">{result.news_count}</p>
            </div>
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
              <p className="text-sm text-gray-400">Recommendation</p>
              <p className="text-sm font-medium mt-1">{result.recommendation}</p>
            </div>
          </div>

          {/* Sentiment Breakdown */}
          <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
            <h2 className="text-lg font-semibold mb-4">Sentiment Breakdown</h2>
            <div className="grid grid-cols-3 gap-4">
              <div className="bg-green-500/10 rounded-lg p-4 text-center">
                <TrendingUp className="mx-auto text-green-400 mb-2" size={24} />
                <p className="text-3xl font-bold text-green-400">{result.positive_news}</p>
                <p className="text-sm text-gray-400">Positive</p>
              </div>
              <div className="bg-red-500/10 rounded-lg p-4 text-center">
                <TrendingDown className="mx-auto text-red-400 mb-2" size={24} />
                <p className="text-3xl font-bold text-red-400">{result.negative_news}</p>
                <p className="text-sm text-gray-400">Negative</p>
              </div>
              <div className="bg-yellow-500/10 rounded-lg p-4 text-center">
                <Minus className="mx-auto text-yellow-400 mb-2" size={24} />
                <p className="text-3xl font-bold text-yellow-400">{result.neutral_news}</p>
                <p className="text-sm text-gray-400">Neutral</p>
              </div>
            </div>
          </div>

          {/* Top Headlines */}
          <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
            <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <Newspaper size={20} className="text-blue-400" />
              Top Headlines
            </h2>
            <div className="space-y-3">
              {result.top_headlines.map((headline, idx) => (
                <div key={idx} className="flex items-start gap-3 p-3 bg-gray-800 rounded-lg">
                  <span className="text-blue-400 font-bold">{idx + 1}</span>
                  <p className="text-gray-200">{headline}</p>
                </div>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  );
}
