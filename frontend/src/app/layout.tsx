import './globals.css';
import { Inter } from 'next/font/google';
import { ReactNode } from 'react';
import Providers from '../components/Providers';

const inter = Inter({ subsets: ['latin'] });

export const metadata = {
  title: 'FinTech Behavioral Guidance Platform',
  description: 'Secure financial insights and behavioral coaching',
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en" className={inter.className}>
      <body className="bg-white text-neutral-800">
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
