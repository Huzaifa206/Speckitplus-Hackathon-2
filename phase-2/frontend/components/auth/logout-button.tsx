'use client';

import React from 'react';
import { Button } from '@/components/ui/button';
import { useAuth } from './auth-context';
import { useToast } from '@/components/ui/use-toast';

const LogoutButton: React.FC = () => {
  const { signOut } = useAuth();
  const { toast } = useToast();

  const handleLogout = async () => {
    try {
      await signOut();
      toast({
        title: 'Logged Out',
        description: 'You have been successfully logged out.',
      });
      // The page will automatically redirect or update based on the auth context
    } catch (error) {
      toast({
        title: 'Logout Failed',
        description: 'There was an issue logging out. Please try again.',
        variant: 'destructive',
      });
    }
  };

  return (
    <Button onClick={handleLogout} variant="outline">
      Logout
    </Button>
  );
};

export default LogoutButton;