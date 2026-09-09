"use client";

import React, { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { apiClient } from "@/lib/api";
import { Dialog, DialogPanel, DialogTitle } from "@headlessui/react";
import { Pie } from "react-chartjs-2";
import "chart.js/auto";

export default function DistributionPage() {
  const { data: wealth, isLoading } = useQuery({
    queryKey: ["wealthDistribution"],
    queryFn: () => apiClient.get("/analytics/wealth-distribution").then((res) => res.data),
  });

  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const { data: categoryDetail, isLoading: loadingDetail } = useQuery({
    queryKey: ["categoryDetail", selectedCategory],
    queryFn: () =>
      apiClient
        .get(`/analytics/wealth-distribution/${selectedCategory}`)
        .then((res) => res.data),
    enabled: !!selectedCategory,
  });

  if (isLoading) return <div className="p-8">Loading wealth distribution...</div>;

  return (
    <main className="p-6 bg-white text-gray-800">
      <h1 className="text-2xl font-bold text-primary mb-6">Wealth Distribution</h1>
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {wealth?.categories?.map((cat: string) => (
          <button
            key={cat}
            className="p-4 bg-emerald-50 rounded-lg hover:bg-emerald-100 transition"
            onClick={() => setSelectedCategory(cat)}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Side drawer for details */}
      <Dialog open={!!selectedCategory} onClose={() => setSelectedCategory(null)} className="relative z-50">
        <div className="fixed inset-0 bg-black/30" />
        <DialogPanel className="fixed right-0 top-0 h-full w-full max-w-md bg-white shadow-xl p-6 overflow-y-auto">
          <DialogTitle className="text-xl font-semibold mb-4">
            {selectedCategory}
          </DialogTitle>
          {loadingDetail ? (
            <div>Loading details…</div>
          ) : (
            <>
              {/* Pie chart */}
              <Pie
                data={{
                  labels: categoryDetail?.pie_chart_data?.map((d) => d.name) ?? [],
                  datasets: [
                    {
                      data: categoryDetail?.pie_chart_data?.map((d) => d.amount) ?? [],
                      backgroundColor: ["#34d399", "#f87171", "#fbbf24", "#60a5fa"],
                    },
                  ],
                }}
                options={{ plugins: { legend: { position: "bottom" } } }}
              />

              {/* Transaction list */}
              <h2 className="mt-4 font-medium">Transactions</h2>
              <ul className="mt-2 space-y-2">
                {categoryDetail?.transactions?.map((tx) => (
                  <li key={tx.id} className="border-b pb-2">
                    <div className="flex justify-between items-center">
                      <div>
                        <p className="font-medium">{tx.merchant}</p>
                        <p className="text-sm text-gray-500">{tx.raw_narration}</p>
                      </div>
                      <div className="text-right">
                        <p className="font-semibold">${tx.amount.toFixed(2)}</p>
                        <span
                          className={`inline-block px-2 py-0.5 text-xs rounded ${
                            tx.necessity_tier === "Necessary"
                              ? "bg-emerald-100 text-emerald-800"
                              : tx.necessity_tier === "Unnecessary"
                              ? "bg-red-100 text-red-800"
                              : tx.necessity_tier === "Important"
                              ? "bg-amber-100 text-amber-800"
                              : "bg-blue-100 text-blue-800"
                          }`}
                        >
                          {tx.necessity_tier}
                        </span>
                      </div>
                    </div>
                    <p className="mt-1 text-xs text-gray-600">{tx.reasoning}</p>
                  </li>
                ))}
              </ul>
            </>
          )}
          <button
            onClick={() => setSelectedCategory(null)}
            className="mt-4 w-full py-2 bg-emerald-600 text-white rounded hover:bg-emerald-700"
          >
            Close
          </button>
        </DialogPanel>
      </Dialog>
    </main>
  );
}
