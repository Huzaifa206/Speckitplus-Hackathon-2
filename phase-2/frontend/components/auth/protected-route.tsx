'use client';

import React from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/components/auth/auth-context';
import { Skeleton } from '@/components/ui/skeleton';

interface ProtectedRouteProps {
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({
  children,
  fallback = (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <Skeleton className="h-10 w-64 mb-4" />
      <Skeleton className="h-4 w-48 mb-2" />
      <Skeleton className="h-16 w-16 rounded-full" />
    </div>
  )
}) => {
  const { user, loading } = useAuth();
  const router = useRouter();

  if (loading) {
    return fallback;
  }

  if (!user) {
    // Redirect to login if not authenticated
    router.push('/login');
    return fallback;
  }

  return <>{children}</>;
};

export default ProtectedRoute;