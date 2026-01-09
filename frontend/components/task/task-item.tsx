'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Task } from '@/lib/types';
import { Trash2, CheckCircle2, Circle } from 'lucide-react';
import ConfirmationModal from './confirmation-modal';

interface TaskItemProps {
  task: Task;
  onUpdate: (task: Task) => void;
  onDelete: (taskId: number) => void;
}

export function TaskItem({ task, onUpdate, onDelete }: TaskItemProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editText, setEditText] = useState(task.title);
  const [showDeleteModal, setShowDeleteModal] = useState(false);

  const handleToggleComplete = () => {
    onUpdate({
      ...task,
      completed: !task.completed,
    });
  };

  const handleSaveEdit = () => {
    if (editText.trim()) {
      onUpdate({
        ...task,
        title: editText.trim(),
      });
      setIsEditing(false);
    }
  };

  const handleCancelEdit = () => {
    setEditText(task.title);
    setIsEditing(false);
  };

  const handleDeleteClick = () => {
    setShowDeleteModal(true);
  };

  const handleDeleteConfirm = () => {
    onDelete(task.id);
  };

  const getPriorityColor = (priority: string) => {
    switch (priority.toLowerCase()) {
      case 'high':
        return 'bg-red-500 hover:bg-red-600';
      case 'medium':
        return 'bg-yellow-500 hover:bg-yellow-600';
      case 'low':
        return 'bg-blue-500 hover:bg-blue-600';
      default:
        return 'bg-gray-500 hover:bg-gray-600';
    }
  };

  return (
    <div className="flex items-center gap-4 p-4 border rounded-lg shadow-sm hover:shadow-md transition-shadow">
      <Button
        variant="ghost"
        size="sm"
        onClick={handleToggleComplete}
        className="h-8 w-8 p-0"
      >
        {task.completed ? (
          <CheckCircle2 className="h-5 w-5 text-green-500" />
        ) : (
          <Circle className="h-5 w-5 text-gray-400" />
        )}
      </Button>

      <div className="flex-1">
        {isEditing ? (
          <input
            type="text"
            value={editText}
            onChange={(e) => setEditText(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter') handleSaveEdit();
              if (e.key === 'Escape') handleCancelEdit();
            }}
            onBlur={handleSaveEdit}
            className="w-full border rounded px-2 py-1"
            autoFocus
          />
        ) : (
          <div>
            <span className={`${task.completed ? 'line-through text-muted-foreground' : ''}`}>
              {task.title}
            </span>
            {task.description && (
              <p className="text-sm text-muted-foreground mt-1">{task.description}</p>
            )}
          </div>
        )}

        <div className="flex items-center gap-2 mt-2">
          {task.priority && (
            <Badge className={`px-2 py-1 ${getPriorityColor(task.priority)}`}>
              {task.priority}
            </Badge>
          )}

          {task.tags && task.tags.length > 0 && (
            <div className="flex gap-1">
              {task.tags.map((tag, index) => (
                <Badge key={index} variant="secondary" className="px-2 py-1">
                  {tag}
                </Badge>
              ))}
            </div>
          )}

          {task.due_date && (
            <span className="text-xs bg-muted px-2 py-1 rounded">
              Due: {new Date(task.due_date).toLocaleDateString()}
            </span>
          )}
        </div>
      </div>

      <div className="flex gap-2">
        <Button
          variant="outline"
          size="sm"
          onClick={() => setIsEditing(!isEditing)}
        >
          {isEditing ? 'Save' : 'Edit'}
        </Button>
        <Button
          variant="outline"
          size="sm"
          onClick={handleDeleteClick}
          className="text-destructive hover:text-destructive"
        >
          <Trash2 className="h-4 w-4" />
        </Button>
      </div>

      <ConfirmationModal
        isOpen={showDeleteModal}
        onClose={() => setShowDeleteModal(false)}
        onConfirm={handleDeleteConfirm}
        title="Delete Task"
        description={`Are you sure you want to delete the task "${task.title}"? This action cannot be undone.`}
        confirmText="Delete"
        cancelText="Cancel"
      />
    </div>
  );
}