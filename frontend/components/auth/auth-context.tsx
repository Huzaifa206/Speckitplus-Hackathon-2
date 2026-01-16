'use client';

import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { User } from '@/lib/types';
import { apiClient } from '@/lib/api';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  signIn: (email: string, password: string) => Promise<void>;
  signUp: (email: string, password: string, name: string) => Promise<void>;
  signOut: () => Promise<void>;
  updateUser: (userData: Partial<User>) => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  // Check for existing session on mount
  useEffect(() => {
    const checkSession = async () => {
      try {
        // Check if user is already logged in by verifying token or session
        const token = localStorage.getItem('auth_token');
        if (token) {
          // Get API base URL from environment or default
          const apiUrl = process.env.NEXT_PUBLIC_API_URL || process.env.BACKEND_URL || 'http://localhost:8000';

          // Verify token with backend using a direct fetch since we don't have user ID yet
          const response = await fetch(`${apiUrl}/api/auth/me`, {
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json',
            },
          });

          if (response.ok) {
            const userData = await response.json();
            setUser(userData);
          } else {
            // Token is invalid, remove it
            localStorage.removeItem('auth_token');
          }
        }
      } catch (error) {
        console.error('Error checking session:', error);
        localStorage.removeItem('auth_token');
      } finally {
        setLoading(false);
      }
    };

    checkSession();
  }, []);

  const signIn = async (email: string, password: string) => {
    try {
      // Use the API client for login
      const data = await apiClient.login(email, password);

      // The API returns { access_token, token_type }
      const { access_token: token } = data;

      // Get API base URL from environment or default
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || process.env.BACKEND_URL || 'http://localhost:8000';

      // Fetch user data after successful login
      const userResponse = await fetch(`${apiUrl}/api/auth/me`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (userResponse.ok) {
        const userData = await userResponse.json();

        // Store token in localStorage (this is already done in the API client)
        setUser(userData);
      } else {
        throw new Error('Failed to fetch user data after login');
      }
    } catch (error) {
      console.error('Sign in error:', error);
      throw error;
    }
  };

  const signUp = async (email: string, password: string, name: string) => {
    try {
      // Use the API client for registration
      const data = await apiClient.register(email, name, password);

      // The API returns { access_token, token_type }
      const { access_token: token } = data;

      // Get API base URL from environment or default
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || process.env.BACKEND_URL || 'http://localhost:8000';

      // Fetch user data after successful registration
      const userResponse = await fetch(`${apiUrl}/api/auth/me`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (userResponse.ok) {
        const userData = await userResponse.json();

        // Store token in localStorage (this is already done in the API client)
        setUser(userData);
      } else {
        throw new Error('Failed to fetch user data after registration');
      }
    } catch (error) {
      console.error('Sign up error:', error);
      throw error;
    }
  };

  const signOut = async () => {
    try {
      // Clear token from localStorage
      localStorage.removeItem('auth_token');
      // Clear any other stored user data
      setUser(null);
    } catch (error) {
      console.error('Sign out error:', error);
    }
  };

  const updateUser = (userData: Partial<User>) => {
    setUser(prevUser => (prevUser ? { ...prevUser, ...userData } : null));
  };

  const value = {
    user,
    loading,
    signIn,
    signUp,
    signOut,
    updateUser,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};