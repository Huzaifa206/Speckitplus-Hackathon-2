export interface Task {
  id: number;
  user_id: string;
  title: string;
  description?: string;
  completed: boolean;
  priority: 'high' | 'medium' | 'low';
  tags: string[];
  due_date: string | null;
  is_recurring: boolean;
  recurring_interval: 'daily' | 'weekly' | null;
  created_at: string;
}

export interface User {
  id: string;
  email: string;
  name: string;
  created_at: string;
  updated_at: string;
}