'use client';

import React from 'react';
import { useAuth } from '@/components/auth/auth-context';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import Navbar from '@/components/navbar';

const HomePage: React.FC = () => {
  const { user, loading } = useAuth();
  const router = useRouter();

  // If user is authenticated, redirect to dashboard
  if (!loading && user) {
    router.push('/dashboard');
    return null; // Render nothing while redirecting
  }

  // If still loading, show a loading state
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-lg">Loading...</div>
      </div>
    );
  }

  // If not authenticated, show welcome page with login/signup options
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <main className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
        <div className="text-center py-12">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">Welcome to Your Task Manager</h2>
          <p className="text-xl text-gray-600 mb-8">
            Organize your tasks efficiently with priorities, tags, and smart filtering
          </p>
          <div className="flex justify-center space-x-4">
            <Link href="/login">
              <Button size="lg">Get Started</Button>
            </Link>
          </div>
        </div>
      </main>
    </div>
  );
};

export default HomePage;