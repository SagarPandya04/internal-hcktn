'use client';

import React from "react";
import { useQuery } from "@tanstack/react-query";
import { apiClient } from "@/lib/api";
import TransactionTable from "@/components/TransactionTable";
import { logout } from "@/lib/auth";

export default function DashboardPage() {
  const { data: transactions, isLoading: loadingTx, error: queryError } = useQuery({
    queryKey: ["transactions"],
    queryFn: () => apiClient.get("/transactions").then((res) => res.data),
    retry: false,
  });

  return (
    <div className="min-h-screen bg-slate-50 text-neutral-800 pb-16">
      <header className="bg-white border-b border-emerald-100 sticky top-0 z-30 shadow-2xs">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-9 h-9 rounded-lg bg-emerald-600 flex items-center justify-center text-white font-black text-xl shadow-xs">
              🌱
            </div>
            <div>
              <span className="font-bold text-lg text-emerald-950 tracking-tight">
                FinTech Behavioral Guidance
              </span>
              <span className="ml-2 text-2xs px-2 py-0.5 bg-emerald-100 text-emerald-800 rounded-full font-semibold border border-emerald-200">
                PS-02
              </span>
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <span className="text-xs text-neutral-500 hidden sm:inline-block font-mono">
              Role: <span className="font-bold text-emerald-800">User</span>
            </span>
            <button
              onClick={logout}
              className="text-xs font-semibold px-3 py-1.5 rounded-lg text-emerald-700 bg-emerald-50 hover:bg-emerald-100 border border-emerald-200 transition"
            >
              Sign Out
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-8 space-y-8">
        {queryError ? (
          <div className="p-4 bg-red-50 text-red-700 border border-red-200 rounded-lg">
            Error loading transactions. Please try again later.
          </div>
        ) : (
          <TransactionTable transactions={transactions} loading={loadingTx} />
        )}
      </main>
    </div>
  );
}
