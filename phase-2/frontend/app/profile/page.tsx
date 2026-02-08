'use client';

import React from 'react';
import ProtectedRoute from '@/components/auth/protected-route';
import UserProfile from '@/components/auth/user-profile';

const ProfilePage: React.FC = () => {
  return (
    <ProtectedRoute>
      <div className="container mx-auto py-10">
        <h1 className="text-3xl font-bold mb-8">User Profile</h1>
        <UserProfile />
      </div>
    </ProtectedRoute>
  );
};

export default ProfilePage;