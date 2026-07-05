'use client';

import { useState, useEffect } from 'react';
import { Bell, Plus, Trash2, Check } from 'lucide-react';

interface Alert {
  id: number;
  symbol: string;
  alert_type: string;
  target_price: number;
  created_at: string;
  triggered: boolean;
}

export default function AlertsPage() {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [symbol, setSymbol] = useState('');
  const [alertType, setAlertType] = useState('above');
  const [targetPrice, setTargetPrice] = useState('');
  const [triggered, setTriggered] = useState<any[]>([]);

  useEffect(() => {
    fetchAlerts();
  }, []);

  const fetchAlerts = async () => {
    try {
      const data = await fetch('/api/alerts').then(r => r.json());
      setAlerts(data.alerts || []);
    } catch (err) {
      console.error(err);
    }
  };

  const handleAdd = async () => {
    if (!symbol || !targetPrice) return;
    try {
      await fetch('/api/alerts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          symbol: symbol.toUpperCase(),
          alert_type: alertType,
          target_price: parseFloat(targetPrice),
        }),
      });
      setSymbol('');
      setTargetPrice('');
      fetchAlerts();
    } catch (err) {
      console.error(err);
    }
  };

  const handleRemove = async (id: number) => {
    try {
      await fetch(`/api/alerts/${id}`, { method: 'DELETE' });
      fetchAlerts();
    } catch (err) {
      console.error(err);
    }
  };

  const handleCheck = async () => {
    try {
      const data = await fetch('/api/alerts/check', { method: 'POST' }).then(r => r.json());
      setTriggered(data.triggered || []);
      fetchAlerts();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-3xl font-bold">Price Alerts</h1>
        <p className="text-gray-400 mt-1">Set alerts for your target prices</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Add Alert */}
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
          <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <Plus size={20} className="text-blue-400" />
            Add New Alert
          </h2>
          <div className="space-y-4">
            <input
              type="text"
              value={symbol}
              onChange={(e) => setSymbol(e.target.value.toUpperCase())}
              placeholder="Stock Symbol (e.g., AAPL)"
              className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500"
            />
            <select
              value={alertType}
              onChange={(e) => setAlertType(e.target.value)}
              className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-blue-500"
            >
              <option value="above">Price Goes Above</option>
              <option value="below">Price Goes Below</option>
            </select>
            <input
              type="number"
              value={targetPrice}
              onChange={(e) => setTargetPrice(e.target.value)}
              placeholder="Target Price ($)"
              className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500"
            />
            <button
              onClick={handleAdd}
              disabled={!symbol || !targetPrice}
              className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 disabled:cursor-not-allowed rounded-lg px-4 py-3 font-medium transition-colors"
            >
              Add Alert
            </button>
          </div>
        </div>

        {/* Active Alerts */}
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-lg font-semibold flex items-center gap-2">
              <Bell size={20} className="text-yellow-400" />
              Active Alerts
            </h2>
            <button
              onClick={handleCheck}
              className="text-sm bg-gray-800 hover:bg-gray-700 px-3 py-1 rounded-lg transition-colors"
            >
              Check Now
            </button>
          </div>

          {alerts.filter(a => !a.triggered).length === 0 ? (
            <p className="text-gray-500 text-center py-8">No active alerts</p>
          ) : (
            <div className="space-y-3">
              {alerts.filter(a => !a.triggered).map((alert) => (
                <div key={alert.id} className="flex items-center justify-between p-3 bg-gray-800 rounded-lg">
                  <div>
                    <p className="font-semibold">{alert.symbol}</p>
                    <p className="text-sm text-gray-400">
                      {alert.alert_type === 'above' ? '↑ Above' : '↓ Below'} ${alert.target_price.toFixed(2)}
                    </p>
                  </div>
                  <button
                    onClick={() => handleRemove(alert.id)}
                    className="text-red-400 hover:text-red-300 p-2"
                  >
                    <Trash2 size={18} />
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Triggered Alerts */}
      {triggered.length > 0 && (
        <div className="bg-green-500/10 border border-green-500/30 rounded-xl p-6">
          <h2 className="text-lg font-semibold mb-3 flex items-center gap-2 text-green-400">
            <Check size={20} />
            Triggered Alerts
          </h2>
          <div className="space-y-2">
            {triggered.map((t: any, idx: number) => (
              <div key={idx} className="p-3 bg-green-500/10 rounded-lg">
                <p className="text-green-400 font-medium">{t.message}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
