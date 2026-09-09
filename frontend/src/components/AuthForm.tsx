'use client';

import { useState } from 'react';
import { login, register } from '../lib/api';

export default function AuthForm({ mode }: { mode: 'login' | 'register' }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [role, setRole] = useState('user');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      if (mode === 'login') {
        await login(email, password);
      } else {
        await register(email, password, fullName, role);
        await login(email, password);
      }
      window.location.href = '/dashboard';
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'An error occurred during authentication.');
    } finally {
      setLoading(false);
    }
  };

  const handleDemoLogin = async () => {
    setError(null);
    setLoading(true);
    try {
      await login('user@fintech.com', 'user12345');
      window.location.href = '/dashboard';
    } catch (err: any) {
      console.error('Demo login error:', err);
      setError(err?.response?.data?.detail || 'Demo login failed. Make sure backend is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center p-4">
      <div className="max-w-md w-full bg-white rounded-2xl p-8 shadow-md border border-emerald-100 space-y-6">
        <div className="text-center space-y-2">
          <div className="w-12 h-12 bg-emerald-600 rounded-xl flex items-center justify-center mx-auto text-white text-2xl shadow-xs">
            🌱
          </div>
          <h2 className="text-2xl font-black text-emerald-950 capitalize tracking-tight">
            {mode === 'login' ? 'Sign In to Your Account' : 'Create an Account'}
          </h2>
          <p className="text-xs text-neutral-500">
            FinTech Behavioral Guidance & Wealth Platform
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-emerald-900 mb-1">
              Email Address
            </label>
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="user@domain.com"
              className="w-full border border-neutral-300 rounded-lg px-3.5 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
            />
          </div>

          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-emerald-900 mb-1">
              Password
            </label>
            <input
              type="password"
              required
              minLength={8}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              className="w-full border border-neutral-300 rounded-lg px-3.5 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
            />
          </div>

          {mode === 'register' && (
            <>
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-emerald-900 mb-1">
                  Full Name
                </label>
                <input
                  type="text"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  placeholder="Alex Morgan"
                  className="w-full border border-neutral-300 rounded-lg px-3.5 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
                />
              </div>

              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-emerald-900 mb-1">
                  Access Role
                </label>
                <select
                  value={role}
                  onChange={(e) => setRole(e.target.value)}
                  className="w-full border border-neutral-300 rounded-lg px-3.5 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 bg-white"
                >
                  <option value="user">User (Personal Transactions)</option>
                  <option value="advisor">Advisor (Read-only Financial Reports)</option>
                  <option value="admin">Admin (System Analytics & RBAC)</option>
                </select>
              </div>
            </>
          )}

          {error && (
            <div className="p-3 bg-rose-50 border border-rose-200 text-rose-700 text-xs rounded-lg font-medium">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-emerald-600 text-white font-bold py-2.5 rounded-lg hover:bg-emerald-700 active:bg-emerald-800 transition shadow-xs disabled:opacity-50 text-sm cursor-pointer"
          >
            {loading ? 'Processing...' : mode === 'login' ? 'Sign In' : 'Create Account'}
          </button>
        </form>

        <div className="relative flex py-1 items-center">
          <div className="flex-grow border-t border-neutral-200"></div>
          <span className="flex-shrink mx-3 text-2xs text-neutral-400 font-semibold uppercase">Or Quick Access</span>
          <div className="flex-grow border-t border-neutral-200"></div>
        </div>

        <button
          type="button"
          onClick={handleDemoLogin}
          disabled={loading}
          className="w-full border-2 border-emerald-600 text-emerald-700 font-bold py-2.5 rounded-lg hover:bg-emerald-50 active:bg-emerald-100 transition text-xs flex items-center justify-center gap-2 cursor-pointer shadow-xs"
        >
          <span>🚀</span> Log In as Pre-loaded Demo User
        </button>

        <div className="text-center text-xs text-neutral-500 pt-2 border-t border-neutral-100">
          {mode === 'login' ? (
            <p>
              Don't have an account?{' '}
              <a href="/register" className="font-bold text-emerald-700 hover:underline">
                Register here
              </a>
            </p>
          ) : (
            <p>
              Already have an account?{' '}
              <a href="/login" className="font-bold text-emerald-700 hover:underline">
                Sign in
              </a>
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
