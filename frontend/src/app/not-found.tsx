'use client';

export default function NotFound() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4">
      <div className="max-w-md w-full bg-white rounded-xl shadow-md border border-gray-200 p-6 text-center">
        <h1 className="text-2xl font-bold text-gray-800 mb-2">Page Not Found</h1>
        <p className="text-sm text-gray-600 mb-4">The page you are looking for does not exist.</p>
        <a href="/" className="inline-block px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300 transition">
          Go Home
        </a>
      </div>
    </div>
  );
}
