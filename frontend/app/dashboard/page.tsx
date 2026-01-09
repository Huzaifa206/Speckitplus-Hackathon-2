'use client';

import React from 'react';
import ProtectedRoute from '@/components/auth/protected-route';
import TaskDashboard from '@/components/task/task-dashboard';
import Navbar from '@/components/navbar';

const DashboardPage: React.FC = () => {
  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <main className="container mx-auto py-10">
          <h1 className="text-3xl font-bold mb-8">Task Dashboard</h1>
          <TaskDashboard />
        </main>
      </div>
    </ProtectedRoute>
  );
};

export default DashboardPage;