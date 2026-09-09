import React from 'react';
import { TransactionRead } from '../types';

interface Props {
  transactions?: TransactionRead[];
  loading: boolean;
}

export default function TransactionTable({ transactions, loading }: Props) {
  if (loading) {
    return (
      <div className="bg-white rounded-xl p-6 shadow-sm border border-emerald-100 text-center text-neutral-500">
        Loading transaction ledger...
      </div>
    );
  }

  const getCategoryBadge = (cat?: string) => {
    switch (cat) {
      case 'Needs':
        return 'bg-emerald-100 text-emerald-800 border-emerald-200';
      case 'Debt':
        return 'bg-amber-100 text-amber-800 border-amber-200';
      case 'Wants':
        return 'bg-purple-100 text-purple-800 border-purple-200';
      case 'Investments':
        return 'bg-blue-100 text-blue-800 border-blue-200';
      default:
        return 'bg-neutral-100 text-neutral-700 border-neutral-200';
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-emerald-100 overflow-hidden">
      <div className="p-5 border-b border-emerald-100 flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-emerald-900">Smart Transaction Ledger</h2>
          <p className="text-xs text-emerald-700/70 mt-0.5">
            Normalized narrations & multi-tier categorizations
          </p>
        </div>
        <span className="text-xs font-semibold px-3 py-1 bg-emerald-50 text-emerald-700 rounded-full border border-emerald-200">
          {transactions?.length ?? 0} Transactions
        </span>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-emerald-50/50 text-xs font-semibold text-emerald-900 uppercase tracking-wider border-b border-emerald-100">
              <th className="py-3 px-4">Date</th>
              <th className="py-3 px-4">Merchant / Raw Narration</th>
              <th className="py-3 px-4">Category</th>
              <th className="py-3 px-4 text-right">Amount</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-emerald-50 text-sm">
            {transactions && transactions.length > 0 ? (
              transactions.map((tx) => (
                <tr key={tx.id} className="hover:bg-emerald-50/30 transition-colors">
                  <td className="py-3 px-4 text-neutral-500 font-mono text-xs whitespace-nowrap">
                    {new Date(tx.timestamp).toLocaleDateString(undefined, {
                      month: 'short',
                      day: 'numeric',
                      year: 'numeric',
                    })}
                  </td>
                  <td className="py-3 px-4">
                    <div className="font-semibold text-neutral-900">
                      {tx.cleaned_merchant || 'Unidentified Merchant'}
                    </div>
                    <div className="text-xs text-neutral-400 font-mono truncate max-w-xs">
                      {tx.raw_narration}
                    </div>
                  </td>
                  <td className="py-3 px-4 whitespace-nowrap">
                    <span className={`inline-block px-2.5 py-0.5 text-xs font-semibold rounded-full border ${getCategoryBadge(tx.category)}`}>
                      {tx.category || 'Uncategorized'}
                    </span>
                  </td>
                  <td className={`py-3 px-4 text-right font-mono font-bold whitespace-nowrap ${tx.type === 'credit' ? 'text-emerald-600' : 'text-neutral-900'}`}>
                    {tx.type === 'credit' ? '+' : '-'}${tx.amount.toFixed(2)}
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={4} className="py-8 text-center text-neutral-500 text-sm">
                  No transactions recorded yet.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
