import React, { useEffect, useState } from 'react';
import { apiClient } from '../lib/api';
import { SimulationResult } from '../types';

interface Props {
  reduction: number;
  setReduction: (val: number) => void;
}

export default function CompromiseSlider({ reduction, setReduction }: Props) {
  const [simulation, setSimulation] = useState<SimulationResult | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchSim = async () => {
      setLoading(true);
      try {
        const res = await apiClient.post(`/analytics/simulate?reduction_percent=${reduction}`);
        setSimulation(res.data);
      } catch (err) {
        console.error("Simulation failed", err);
      } finally {
        setLoading(false);
      }
    };
    fetchSim();
  }, [reduction]);

  return (
    <div className="bg-white rounded-xl p-6 shadow-sm border border-emerald-100 space-y-6">
      <div>
        <h2 className="text-xl font-bold text-emerald-900">Compromise & Wealth Simulator</h2>
        <p className="text-xs text-emerald-700/70 mt-0.5">
          Tweak discretionary spend cuts (0% - 50%) to project long-term compound wealth
        </p>
      </div>

      {/* Interactive Slider */}
      <div className="space-y-3 p-4 bg-emerald-50/60 rounded-lg border border-emerald-100">
        <div className="flex justify-between items-center text-sm">
          <label className="font-semibold text-emerald-900">Discretionary Spend Cut:</label>
          <span className="px-3 py-1 bg-emerald-600 text-white font-bold rounded-md text-base">
            {reduction}%
          </span>
        </div>
        <input
          type="range"
          min="0"
          max="50"
          step="5"
          value={reduction}
          onChange={(e) => setReduction(Number(e.target.value))}
          className="w-full h-2 bg-emerald-200 rounded-lg appearance-none cursor-pointer accent-emerald-600"
        />
        <div className="flex justify-between text-xs text-emerald-700 font-medium">
          <span>0% (No change)</span>
          <span>25% (Moderate)</span>
          <span>50% (Aggressive)</span>
        </div>
      </div>

      {/* Freed Capital Display */}
      <div className="flex items-center justify-between p-4 bg-emerald-100/60 rounded-lg border border-emerald-200">
        <div>
          <p className="text-xs font-semibold text-emerald-800 uppercase tracking-wider">Monthly Freed Capital (ΔS)</p>
          <p className="text-xs text-emerald-700">Reallocated from non-essential wants</p>
        </div>
        <p className="text-2xl font-black text-emerald-800">
          +${simulation?.delta_savings?.toFixed(2) ?? '0.00'}/mo
        </p>
      </div>

      {/* Future Value Compound Wealth Forecaster */}
      <div className="space-y-2">
        <h3 className="text-xs font-bold uppercase tracking-wider text-emerald-800">
          📈 8% Annual Annuity Wealth Projections
        </h3>
        <div className="grid grid-cols-3 gap-3">
          <div className="p-3 bg-white border border-emerald-200 rounded-lg text-center shadow-2xs">
            <p className="text-xs text-neutral-500 font-medium">1 Year</p>
            <p className="text-base font-bold text-emerald-700 mt-1">
              ${simulation?.future_value_1y?.toLocaleString() ?? '0'}
            </p>
          </div>
          <div className="p-3 bg-white border border-emerald-200 rounded-lg text-center shadow-2xs">
            <p className="text-xs text-neutral-500 font-medium">3 Years</p>
            <p className="text-base font-bold text-emerald-700 mt-1">
              ${simulation?.future_value_3y?.toLocaleString() ?? '0'}
            </p>
          </div>
          <div className="p-3 bg-emerald-700 text-white rounded-lg text-center shadow-sm">
            <p className="text-xs text-emerald-200 font-medium">5 Years</p>
            <p className="text-base font-extrabold mt-1">
              ${simulation?.future_value_5y?.toLocaleString() ?? '0'}
            </p>
          </div>
        </div>
      </div>

      {/* Debt Prepayment Acceleration */}
      {simulation && simulation.tenure_reduction_months > 0 && (
        <div className="p-3 rounded-lg bg-amber-50 border border-amber-200 text-xs space-y-1">
          <p className="font-bold text-amber-900 flex items-center gap-1">
            <span>⚡</span> Loan Acceleration Impact
          </p>
          <p className="text-amber-800">
            Diverting ${simulation.delta_savings}/mo cuts debt tenure by{' '}
            <span className="font-bold text-amber-950">{simulation.tenure_reduction_months} months</span> and saves{' '}
            <span className="font-bold text-amber-950">${simulation.interest_saved.toLocaleString()}</span> in total interest!
          </p>
        </div>
      )}
    </div>
  );
}
