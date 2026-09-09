import React from 'react';
import { CashFlowSummary, DebtMetrics, BehavioralInsights } from '../types';

interface Props {
  cashflow?: CashFlowSummary;
  debt?: DebtMetrics;
  insights?: BehavioralInsights;
  loading: boolean;
}

export default function AnalyticsSummary({ cashflow, debt, insights, loading }: Props) {
  if (loading) {
    return (
      <div className="bg-white rounded-xl p-6 shadow-sm border border-emerald-100 flex items-center justify-center min-h-[300px]">
        <div className="flex items-center space-x-3 text-emerald-700 font-medium">
          <svg className="animate-spin h-5 w-5 text-emerald-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span>Loading Financial Intelligence...</span>
        </div>
      </div>
    );
  }

  const dtiVal = debt?.dti ?? 0;
  let dtiTier = "Healthy";
  let dtiColor = "bg-emerald-100 text-emerald-800 border-emerald-200";
  if (dtiVal >= 45) {
    dtiTier = "High Risk";
    dtiColor = "bg-rose-100 text-rose-800 border-rose-200";
  } else if (dtiVal >= 30) {
    dtiTier = "Moderate";
    dtiColor = "bg-amber-100 text-amber-800 border-amber-200";
  }

  return (
    <div className="bg-white rounded-xl p-6 shadow-sm border border-emerald-100 space-y-6">
      <div className="flex items-center justify-between border-b border-emerald-100 pb-4">
        <div>
          <h2 className="text-xl font-bold text-emerald-900">Financial Overview</h2>
          <p className="text-xs text-emerald-700/70 mt-0.5">Real-time cashflow velocity & debt metrics</p>
        </div>
        <span className={`px-3 py-1 text-xs font-semibold rounded-full border ${dtiColor}`}>
          DTI Risk: {dtiTier}
        </span>
      </div>

      {/* Grid of Key Metrics */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {/* Cashflow Velocity Card */}
        <div className="p-4 rounded-lg bg-emerald-50/50 border border-emerald-100/80 space-y-2">
          <p className="text-xs font-semibold uppercase tracking-wider text-emerald-800">Cash Flow Velocity</p>
          <div className="flex justify-between items-baseline">
            <span className="text-sm text-neutral-600">Daily Earn:</span>
            <span className="text-base font-bold text-emerald-700">${cashflow?.daily_earn?.toFixed(2) ?? '0.00'}</span>
          </div>
          <div className="flex justify-between items-baseline">
            <span className="text-sm text-neutral-600">Daily Burn:</span>
            <span className="text-base font-bold text-neutral-800">${cashflow?.daily_burn?.toFixed(2) ?? '0.00'}</span>
          </div>
          <div className="flex justify-between items-baseline pt-2 border-t border-emerald-100">
            <span className="text-sm font-medium text-emerald-900">Net Monthly Margin:</span>
            <span className="text-base font-extrabold text-emerald-600">${cashflow?.monthly_net_margin?.toFixed(2) ?? '0.00'}</span>
          </div>
        </div>

        {/* Debt Drag & EMI Card */}
        <div className="p-4 rounded-lg bg-emerald-50/50 border border-emerald-100/80 space-y-2">
          <p className="text-xs font-semibold uppercase tracking-wider text-emerald-800">Debt & EMI Intelligence</p>
          <div className="flex justify-between items-baseline">
            <span className="text-sm text-neutral-600">Debt-to-Income (DTI):</span>
            <span className="text-base font-bold text-neutral-900">{debt?.dti?.toFixed(1) ?? '0'}%</span>
          </div>
          <div className="flex justify-between items-baseline">
            <span className="text-sm text-neutral-600">Debt Drag:</span>
            <span className="text-base font-bold text-neutral-800">{debt?.debt_drag_percentage?.toFixed(1) ?? '0'}%</span>
          </div>
          <div className="flex justify-between items-baseline pt-2 border-t border-emerald-100">
            <span className="text-sm font-medium text-emerald-900">Monthly EMI Total:</span>
            <span className="text-base font-extrabold text-neutral-900">${debt?.monthly_emi_total?.toFixed(2) ?? '0.00'}</span>
          </div>
        </div>
      </div>

      {/* Behavioral Patterns */}
      <div className="p-4 rounded-lg bg-emerald-950 text-emerald-50 space-y-3">
        <h3 className="text-sm font-semibold text-emerald-300 flex items-center gap-2">
          <span>🧠</span> Behavioral Insights & Triggers
        </h3>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
          <div className="bg-emerald-900/60 p-2.5 rounded border border-emerald-800">
            <p className="text-emerald-300 font-medium">Weekend Spend Spike</p>
            <p className="text-sm font-bold mt-1 text-white">
              {insights?.weekend_spike ? '⚡ Detected' : '✅ Normal'}
            </p>
          </div>
          <div className="bg-emerald-900/60 p-2.5 rounded border border-emerald-800">
            <p className="text-emerald-300 font-medium">Post-Payday Surge</p>
            <p className="text-sm font-bold mt-1 text-white">
              {insights?.post_payday_surge ? '⚠️ Detected' : '✅ Stable'}
            </p>
          </div>
          <div className="bg-emerald-900/60 p-2.5 rounded border border-emerald-800">
            <p className="text-emerald-300 font-medium">Monthly Subscriptions</p>
            <p className="text-sm font-bold mt-1 text-emerald-400">
              ${insights?.subscription_monthly_total?.toFixed(2) ?? '0.00'}/mo
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
