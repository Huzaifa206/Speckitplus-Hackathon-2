'use client';

import React, { useState, useEffect } from 'react';
import { TaskForm } from './task-form';
import { TaskList } from './task-list';
import { Filters } from './filters';
import { Task } from '@/lib/types';
import { useAuth } from '@/components/auth/auth-context';
import { useToast } from '@/components/ui/use-toast';
import { apiClient } from '@/lib/api';

import { TaskInput } from '@/lib/types';

export const TaskDashboard: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [filteredTasks, setFilteredTasks] = useState<Task[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedPriority, setSelectedPriority] = useState('all');
  const [sortBy, setSortBy] = useState('created_at');
  const { user } = useAuth();
  const { toast } = useToast();

  // Load tasks from API when user changes
  useEffect(() => {
    if (user) {
      loadTasks();
    }
  }, [user]);

  const loadTasks = async () => {
    try {
      if (!user) return;

      const data = await apiClient.getTasks(user.id);
      setTasks(data.tasks || data);
      setFilteredTasks(data.tasks || data);
    } catch (error) {
      console.error('Error loading tasks:', error);
      toast({
        title: 'Error',
        description: 'Failed to load tasks. Please try again.',
        variant: 'destructive',
      });
    }
  };

  // Apply filters and sorting
  useEffect(() => {
    let result = [...tasks];

    // Apply search filter
    if (searchTerm) {
      result = result.filter(task =>
        task.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (task.description && task.description.toLowerCase().includes(searchTerm.toLowerCase())) ||
        (task.tags && Array.isArray(task.tags) && task.tags.some(tag => tag.toLowerCase().includes(searchTerm.toLowerCase())))
      );
    }

    // Apply priority filter
    if (selectedPriority !== 'all') {
      result = result.filter(task => task.priority === selectedPriority);
    }

    // Apply sorting
    result.sort((a, b) => {
      switch (sortBy) {
        case 'due_date':
          if (!a.due_date && !b.due_date) return 0;
          if (!a.due_date) return 1;
          if (!b.due_date) return -1;
          return new Date(a.due_date!).getTime() - new Date(b.due_date!).getTime();
        case 'priority':
          const priorityOrder = { high: 3, medium: 2, low: 1 };
          return priorityOrder[b.priority as keyof typeof priorityOrder] - priorityOrder[a.priority as keyof typeof priorityOrder];
        case 'title':
          return a.title.localeCompare(b.title);
        case 'created_at':
        default:
          return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
      }
    });

    setFilteredTasks(result);
  }, [tasks, searchTerm, selectedPriority, sortBy]);

  const handleTaskSubmit = async (newTask: TaskInput) => {
    try {
      if (!user) return;

      const createdTask = await apiClient.createTask(user.id, newTask);
      setTasks([...tasks, createdTask]);
      toast({
        title: 'Success',
        description: 'Task created successfully!',
      });
    } catch (error) {
      console.error('Error creating task:', error);
      toast({
        title: 'Error',
        description: 'Failed to create task. Please try again.',
        variant: 'destructive',
      });
    }
  };

  const handleTaskUpdate = async (updatedTask: Task) => {
    try {
      if (!user) return;

      const updatedTaskData = await apiClient.updateTask(user.id, updatedTask.id, updatedTask);
      setTasks(tasks.map(task => task.id === updatedTask.id ? updatedTaskData : task));
      toast({
        title: 'Success',
        description: 'Task updated successfully!',
      });
    } catch (error) {
      console.error('Error updating task:', error);
      toast({
        title: 'Error',
        description: 'Failed to update task. Please try again.',
        variant: 'destructive',
      });
    }
  };

  const handleTaskDelete = async (taskId: number) => {
    try {
      if (!user) return;

      await apiClient.deleteTask(user.id, taskId);
      setTasks(tasks.filter(task => task.id !== taskId));
      toast({
        title: 'Success',
        description: 'Task deleted successfully!',
      });
    } catch (error) {
      console.error('Error deleting task:', error);
      toast({
        title: 'Error',
        description: 'Failed to delete task. Please try again.',
        variant: 'destructive',
      });
    }
  };

  const handleSearchChange = (search: string) => {
    setSearchTerm(search);
  };

  const handlePriorityChange = (priority: string) => {
    setSelectedPriority(priority);
  };

  const handleSortChange = (sort: string) => {
    setSortBy(sort);
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div className="lg:col-span-1">
        <div className="bg-white/80 backdrop-blur-sm rounded-xl shadow-sm border border-gray-200/30 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Create New Task</h2>
          <TaskForm onSubmit={handleTaskSubmit} />
        </div>
      </div>

      <div className="lg:col-span-2">
        <div className="bg-white/80 backdrop-blur-sm rounded-xl shadow-sm border border-gray-200/30 p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Filter & Sort Tasks</h2>
          <Filters
            onSearchChange={handleSearchChange}
            onPriorityChange={handlePriorityChange}
            onSortChange={handleSortChange}
          />
        </div>

        <TaskList
          tasks={filteredTasks}
          onTaskUpdate={handleTaskUpdate}
          onTaskDelete={handleTaskDelete}
        />
      </div>
    </div>
  );
};

export default TaskDashboard;