import './globals.css';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import { AuthProvider } from '@/components/auth/auth-context';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Todo App',
  description: 'A modern todo application with advanced organization features',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${inter.className} bg-gradient-to-br from-indigo-50 via-purple-50 to-slate-50 antialiased`}>
        <AuthProvider>
          <div className="w-full">
            {children}
          </div>
        </AuthProvider>
      </body>
    </html>
  );
}