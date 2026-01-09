'use client';

import React from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { useAuth } from '@/components/auth/auth-context';
import { User } from '@/lib/types';

interface NavItem {
  title: string;
  href: string;
}

interface NavbarProps {
  navItems?: NavItem[];
}

const Navbar: React.FC<NavbarProps> = ({ navItems = [] }) => {
  const { user, loading } = useAuth();

  return (
    <nav className="bg-white shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link href="/" className="flex-shrink-0 flex items-center">
              <span className="text-xl font-bold text-indigo-600">Todo App</span>
            </Link>
            <div className="hidden md:ml-6 md:flex md:space-x-8">
              {navItems.map((item) => (
                <Link
                  key={item.href}
                  href={item.href}
                  className="inline-flex items-center px-1 pt-1 border-b-2 border-transparent text-sm font-medium text-gray-500 hover:text-gray-700 hover:border-gray-300"
                >
                  {item.title}
                </Link>
              ))}
            </div>
          </div>
          <div className="flex items-center">
            {loading ? (
              <div className="text-sm text-gray-500">Loading...</div>
            ) : user ? (
              <div className="flex items-center space-x-4">
                <span className="text-sm text-gray-700 hidden sm:block">
                  Welcome, {user.name || user.email}
                </span>
                <Link href="/dashboard">
                  <Button variant="ghost">Dashboard</Button>
                </Link>
                <Link href="/profile">
                  <Button variant="ghost">Profile</Button>
                </Link>
                <Link href="/login">
                  <Button variant="outline">Logout</Button>
                </Link>
              </div>
            ) : (
              <div className="flex space-x-4">
                <Link href="/login">
                  <Button variant="outline">Login</Button>
                </Link>
                <Link href="/login">
                  <Button>Sign Up</Button>
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;