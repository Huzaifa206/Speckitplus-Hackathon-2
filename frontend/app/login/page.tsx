'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import LoginForm from '@/components/auth/login-form';
import SignupForm from '@/components/auth/signup-form';

const LoginPage: React.FC = () => {
  const [showSignup, setShowSignup] = useState(false);

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-slate-50">
      <div className="min-h-screen flex items-center justify-center p-4">
        <div className="w-full max-w-md">
          {!showSignup ? (
            <LoginForm onSwitchToSignup={() => setShowSignup(true)} />
          ) : (
            <SignupForm onSwitchToLogin={() => setShowSignup(false)} />
          )}
          <div className="mt-4 text-center text-sm text-gray-600">
            <Link href="/" className="text-blue-600 hover:text-blue-800 underline">
              Back to Home
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;