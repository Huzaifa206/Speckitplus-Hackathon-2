'use client';

import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { User } from '@/lib/types';

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
          // Verify token with backend
          const response = await fetch('http://localhost:8000/api/auth/me', {
            headers: {
              'Authorization': `Bearer ${token}`,
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
      const response = await fetch('http://localhost:8000/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Sign in failed');
      }

      const data = await response.json();
      const { access_token: token } = data;

      // Get user data after login
      const userResponse = await fetch('http://localhost:8000/api/auth/me', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (userResponse.ok) {
        const userData = await userResponse.json();

        // Store token in localStorage
        localStorage.setItem('auth_token', token);
        setUser(userData);
      }
    } catch (error) {
      console.error('Sign in error:', error);
      throw error;
    }
  };

  const signUp = async (email: string, password: string, name: string) => {
    try {
      const response = await fetch('http://localhost:8000/api/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, name, password }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Sign up failed');
      }

      const data = await response.json();
      const { access_token: token } = data;

      // Get user data after registration
      const userResponse = await fetch('http://localhost:8000/api/auth/me', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (userResponse.ok) {
        const userData = await userResponse.json();

        // Store token in localStorage
        localStorage.setItem('auth_token', token);
        setUser(userData);
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