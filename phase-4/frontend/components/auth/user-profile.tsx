'use client';

import React from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { useAuth } from '@/components/auth/auth-context';
import LogoutButton from '@/components/auth/logout-button';

const UserProfile: React.FC = () => {
  const { user } = useAuth();

  if (!user) {
    return null;
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>User Profile</CardTitle>
      </CardHeader>
      <CardContent className="grid gap-4">
        <div>
          <h3 className="font-medium">Name</h3>
          <p>{user.name || 'N/A'}</p>
        </div>
        <div>
          <h3 className="font-medium">Email</h3>
          <p>{user.email}</p>
        </div>
        <div className="flex justify-end mt-4">
          <LogoutButton />
        </div>
      </CardContent>
    </Card>
  );
};

export default UserProfile;