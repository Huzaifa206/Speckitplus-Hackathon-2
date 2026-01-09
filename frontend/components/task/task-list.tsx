'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { TaskItem } from './task-item';
import { Task } from '@/lib/types';

interface TaskListProps {
  tasks: Task[];
  onTaskUpdate: (task: Task) => void;
  onTaskDelete: (taskId: number) => void;
}

export function TaskList({ tasks, onTaskUpdate, onTaskDelete }: TaskListProps) {
  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>Your Tasks</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {tasks.length === 0 ? (
            <p className="text-center text-muted-foreground">No tasks found. Add a new task to get started!</p>
          ) : (
            tasks.map((task) => (
              <TaskItem
                key={task.id}
                task={task}
                onUpdate={onTaskUpdate}
                onDelete={onTaskDelete}
              />
            ))
          )}
        </div>
      </CardContent>
    </Card>
  );
}