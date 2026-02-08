'use client';

import React from 'react';
import ProtectedRoute from '@/components/auth/protected-route';
import TaskDashboard from '@/components/task/task-dashboard';
import Navbar from '@/components/navbar';

const DashboardPage: React.FC = () => {
  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-slate-50">
        <Navbar />
        <main className="py-8">
          <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="mb-8">
              <h1 className="text-3xl font-bold bg-gradient-to-r from-indigo-600 via-purple-600 to-slate-600 bg-clip-text text-transparent">
                Task Dashboard
              </h1>
              <p className="text-gray-600 mt-2">Manage your tasks with colorful simplicity</p>
            </div>
            <TaskDashboard />
          </div>
        </main>
      </div>
    </ProtectedRoute>
  );
};

export default DashboardPage;