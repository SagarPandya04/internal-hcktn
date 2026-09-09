'use client';

import Link from 'next/link';

export default function ErrorComponent({ error, reset }: { error: Error; reset: () => void }) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-rose-50 p-4">
      <div className="max-w-md w-full bg-white rounded-xl shadow-md border border-rose-200 p-6 text-center">
        <h1 className="text-2xl font-bold text-rose-800 mb-2">Something went wrong</h1>
        <p className="text-sm text-rose-600 mb-4">{error.message}</p>
        <div className="flex gap-2 justify-center">
          <button
            onClick={reset}
            className="px-4 py-2 bg-rose-100 text-rose-800 rounded hover:bg-rose-200 transition"
          >
            Try again
          </button>
          <Link href="/" className="px-4 py-2 bg-rose-600 text-white rounded hover:bg-rose-700 transition">
            Home
          </Link>
        </div>
      </div>
    </div>
  );
}
