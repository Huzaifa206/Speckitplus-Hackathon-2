'use client';

import React from 'react';
import { useAuth } from '@/components/auth/auth-context';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Zap, Shield, Layout } from 'lucide-react'; // Lucide React icons

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

  // If not authenticated, show vibrant landing page
  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-slate-50 overflow-hidden">
      {/* Decorative gradient blobs */}
      <div className="absolute top-20 left-10 w-72 h-72 bg-purple-200 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob"></div>
      <div className="absolute top-1/3 right-10 w-72 h-72 bg-indigo-200 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob animation-delay-2000"></div>
      <div className="absolute bottom-20 left-1/3 w-72 h-72 bg-blue-200 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob animation-delay-4000"></div>

      <div className="relative z-10">
        {/* Glassmorphism Navbar */}
        <nav className="sticky top-0 z-50 bg-white/70 backdrop-blur-md border-b border-gray-200/30">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex items-center">
                <Link href="/" className="flex-shrink-0 flex items-center">
                  <div className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white p-2 rounded-lg font-bold text-xl">
                    Todo<span className="font-light">App</span>
                  </div>
                </Link>
              </div>
              <div className="flex items-center space-x-4">
                <Link href="/login">
                  <Button variant="outline" className="text-indigo-600 border-indigo-600 hover:bg-indigo-50">
                    Login
                  </Button>
                </Link>
                <Link href="/login">
                  <Button className="bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white">
                    Sign Up
                  </Button>
                </Link>
              </div>
            </div>
          </div>
        </nav>

        <main className="py-12">
          {/* Hero Section */}
          <section className="py-20">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <div className="text-center">
                <h1 className="text-5xl md:text-6xl font-extrabold text-slate-900 tracking-tight mb-6">
                  <span className="block">Organize your life with</span>
                  <span className="block bg-gradient-to-r from-indigo-600 via-purple-600 to-indigo-600 bg-clip-text text-transparent mt-2">
                    colorful simplicity
                  </span>
                </h1>
                <p className="text-xl text-slate-600 max-w-3xl mx-auto mb-10">
                  The intelligent task manager that evolves with you.
                  Streamline your workflow and boost your productivity with our intuitive platform.
                </p>
                <div className="flex justify-center">
                  <Link href="/login">
                    <Button size="lg" className="bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white px-8 py-4 rounded-full text-lg font-semibold transform transition-all duration-200 hover:scale-105">
                      Get Started for Free
                    </Button>
                  </Link>
                </div>
              </div>
            </div>
          </section>

          {/* Feature Grid */}
          <section className="py-20">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <div className="text-center mb-16">
                <h2 className="text-3xl font-bold text-slate-900 mb-4">
                  Powerful Features, Simple Interface
                </h2>
                <p className="text-lg text-slate-600 max-w-2xl mx-auto">
                  Everything you need to stay organized and productive
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-10">
                {/* Feature 1 */}
                <div className="bg-white/70 backdrop-blur-sm rounded-2xl p-8 shadow-lg border border-white/30 transform transition-all duration-300 hover:scale-105 hover:shadow-xl">
                  <div className="bg-gradient-to-r from-indigo-500 to-purple-500 p-3 rounded-xl w-14 h-14 flex items-center justify-center mb-6">
                    <Zap className="h-8 w-8 text-white" />
                  </div>
                  <h3 className="text-xl font-bold text-slate-900 mb-3">
                    Lightning Fast
                  </h3>
                  <p className="text-slate-600">
                    Experience blazing-fast performance with our optimized platform.
                    Tasks load instantly, keeping you in the flow.
                  </p>
                </div>

                {/* Feature 2 */}
                <div className="bg-white/70 backdrop-blur-sm rounded-2xl p-8 shadow-lg border border-white/30 transform transition-all duration-300 hover:scale-105 hover:shadow-xl">
                  <div className="bg-gradient-to-r from-indigo-500 to-purple-500 p-3 rounded-xl w-14 h-14 flex items-center justify-center mb-6">
                    <Shield className="h-8 w-8 text-white" />
                  </div>
                  <h3 className="text-xl font-bold text-slate-900 mb-3">
                    Secure by Default
                  </h3>
                  <p className="text-slate-600">
                    Your data is protected with enterprise-grade security.
                    We handle your information with the utmost care.
                  </p>
                </div>

                {/* Feature 3 */}
                <div className="bg-white/70 backdrop-blur-sm rounded-2xl p-8 shadow-lg border border-white/30 transform transition-all duration-300 hover:scale-105 hover:shadow-xl">
                  <div className="bg-gradient-to-r from-indigo-500 to-purple-500 p-3 rounded-xl w-14 h-14 flex items-center justify-center mb-6">
                    <Layout className="h-8 w-8 text-white" />
                  </div>
                  <h3 className="text-xl font-bold text-slate-900 mb-3">
                    Beautifully Simple
                  </h3>
                  <p className="text-slate-600">
                    Clean, intuitive design that makes organizing your tasks effortless.
                    Spend less time managing, more time doing.
                  </p>
                </div>
              </div>
            </div>
          </section>
        </main>
      </div>

      <style jsx>{`
        @keyframes blob {
          0% {
            transform: translate(0px, 0px) scale(1);
          }
          33% {
            transform: translate(30px, -50px) scale(1.1);
          }
          66% {
            transform: translate(-20px, 20px) scale(0.9);
          }
          100% {
            transform: translate(0px, 0px) scale(1);
          }
        }
        .animate-blob {
          animation: blob 7s infinite;
        }
        .animation-delay-2000 {
          animation-delay: 2s;
        }
        .animation-delay-4000 {
          animation-delay: 4s;
        }
      `}</style>
    </div>
  );
};

export default HomePage;