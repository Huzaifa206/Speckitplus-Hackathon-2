'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import LoginForm from '@/components/auth/login-form';
import SignupForm from '@/components/auth/signup-form';

const LoginPage: React.FC = () => {
  const [showSignup, setShowSignup] = useState(false);

  return (
    <div className="min-h-screen flex items-center justify-center bg-muted p-4">
      <div className="w-full max-w-md">
        {!showSignup ? (
          <LoginForm onSwitchToSignup={() => setShowSignup(true)} />
        ) : (
          <SignupForm onSwitchToLogin={() => setShowSignup(false)} />
        )}
        <div className="mt-4 text-center text-sm text-muted-foreground">
          <Link href="/" className="underline underline-offset-4 hover:text-primary">
            Back to Home
          </Link>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;