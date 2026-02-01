'use client';

import React, { useState } from 'react';
import ProtectedRoute from '@/components/auth/protected-route';
import TaskDashboard from '@/components/task/task-dashboard';
import Navbar from '@/components/navbar';
import ChatWidget from '@/components/chat-widget';

const DashboardPage: React.FC = () => {
  const [showChat, setShowChat] = useState(false);

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

            {/* Chat Widget Toggle Button */}
            <div className="fixed bottom-6 right-6 z-50">
              <button
                onClick={() => setShowChat(!showChat)}
                className="bg-indigo-600 hover:bg-indigo-700 text-white p-4 rounded-full shadow-lg transition-all duration-300 transform hover:scale-105"
                aria-label={showChat ? "Close chat" : "Open chat"}
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={showChat ? "M6 18L18 6M6 6l12 12" : "M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"} />
                </svg>
              </button>
            </div>

            {/* Chat Widget as Popup */}
            {showChat && (
              <div className="fixed inset-0 z-40 bg-black bg-opacity-50 flex items-center justify-center p-4">
                <div className="bg-white rounded-xl shadow-2xl w-full max-w-2xl max-h-[80vh] overflow-hidden flex flex-col">
                  <div className="p-4 border-b flex justify-between items-center">
                    <h2 className="text-xl font-semibold">AI Task Assistant</h2>
                    <button
                      onClick={() => setShowChat(false)}
                      className="text-gray-500 hover:text-gray-700"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </button>
                  </div>
                  <div className="flex-grow overflow-auto">
                    <ChatWidget onClose={() => setShowChat(false)} />
                  </div>
                </div>
              </div>
            )}

            {/* Task Dashboard */}
            <div className="w-full">
              <TaskDashboard />
            </div>
          </div>
        </main>
      </div>
    </ProtectedRoute>
  );
};

export default DashboardPage;