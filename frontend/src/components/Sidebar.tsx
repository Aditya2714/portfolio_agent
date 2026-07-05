'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  LayoutDashboard,
  Bot,
  Plus,
  BarChart3,
  GitCompare,
  Newspaper,
  TrendingDown,
  DollarSign,
  Bell,
  FileText
} from 'lucide-react';
import clsx from 'clsx';

const navItems = [
  { href: '/', label: 'Dashboard', icon: LayoutDashboard },
  { href: '/assistant', label: 'AI Assistant', icon: Bot },
  { href: '/holdings', label: 'Manage Holdings', icon: Plus },
  { href: '/research', label: 'Stock Research', icon: BarChart3 },
  { href: '/compare', label: 'Compare Stocks', icon: GitCompare },
  { href: '/sentiment', label: 'Sentiment Analysis', icon: Newspaper },
  { href: '/technical', label: 'Technical Analysis', icon: TrendingDown },
  { href: '/tax', label: 'Tax Optimization', icon: DollarSign },
  { href: '/alerts', label: 'Price Alerts', icon: Bell },
  { href: '/reports', label: 'Reports', icon: FileText },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 bg-gray-900 border-r border-gray-800 flex flex-col">
      {/* Logo */}
      <div className="p-6 border-b border-gray-800">
        <h1 className="text-xl font-bold flex items-center gap-2">
          <span className="text-2xl">💰</span>
          <span className="bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
            AI Portfolio
          </span>
        </h1>
        <p className="text-xs text-gray-500 mt-1">Your AI Financial Advisor</p>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4 space-y-1 overflow-y-auto">
        {navItems.map((item) => {
          const isActive = pathname === item.href;
          const Icon = item.icon;

          return (
            <Link
              key={item.href}
              href={item.href}
              className={clsx(
                'flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200',
                isActive
                  ? 'bg-blue-600/20 text-blue-400 border border-blue-500/30'
                  : 'text-gray-400 hover:bg-gray-800 hover:text-white'
              )}
            >
              <Icon size={20} />
              <span className="text-sm font-medium">{item.label}</span>
            </Link>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-gray-800">
        <div className="bg-gradient-to-r from-blue-600/20 to-cyan-600/20 rounded-lg p-4 border border-blue-500/20">
          <p className="text-xs text-gray-400">Powered by</p>
          <p className="text-sm font-semibold text-white">10 AI Agents</p>
          <p className="text-xs text-gray-500 mt-1">Groq + Llama 3.3</p>
        </div>
      </div>
    </aside>
  );
}
