'use client';

export const logout = () => {
  if (typeof window !== 'undefined') {
    // Clear token from storage
    localStorage.removeItem('access_token');
    // Clear cookie
    document.cookie = 'access_token=; path=/; max-age=0';
    // Redirect to login page
    window.location.href = '/login';
  }
};
