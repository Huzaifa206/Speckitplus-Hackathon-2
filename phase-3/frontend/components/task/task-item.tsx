'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Task } from '@/lib/types';
import { Trash2, CheckCircle2, Circle } from 'lucide-react';
import ConfirmationModal from './confirmation-modal';

interface TaskItemProps {
  task: Task;
  displayIndex: number;
  onUpdate: (task: Task) => void;
  onDelete: (taskId: number) => void;
}

export function TaskItem({ task, displayIndex, onUpdate, onDelete }: TaskItemProps) {
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
        return 'bg-red-50 text-red-800 border-red-200';
      case 'medium':
        return 'bg-amber-50 text-amber-800 border-amber-200';
      case 'low':
        return 'bg-blue-50 text-blue-800 border-blue-200';
      default:
        return 'bg-gray-50 text-gray-800 border-gray-200';
    }
  };

  return (
    <div className={`${task.completed ? 'bg-white' : 'bg-white/80 backdrop-blur-sm'} rounded-xl shadow-sm border border-gray-200 p-4 flex items-start gap-4`}>
      {/* Display Index */}
      <div className="flex-shrink-0 w-8 h-8 bg-indigo-100 rounded-full flex items-center justify-center">
        <span className="text-sm font-bold text-indigo-700">{displayIndex}</span>
      </div>

      <Button
        variant="ghost"
        size="sm"
        onClick={handleToggleComplete}
        className="h-8 w-8 p-0 flex-shrink-0"
      >
        {task.completed ? (
          <CheckCircle2 className="h-5 w-5 text-green-500" />
        ) : (
          <Circle className="h-5 w-5 text-gray-400" />
        )}
      </Button>

      <div className="flex-1 min-w-0">
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
            className="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            autoFocus
          />
        ) : (
          <div>
            <h3 className={`font-semibold ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
              {task.title}
            </h3>
            {task.description && (
              <p className="text-sm text-gray-500 mt-1">{task.description}</p>
            )}
          </div>
        )}

        <div className="flex flex-wrap items-center gap-2 mt-3">
          {task.priority && (
            <Badge className={`${getPriorityColor(task.priority)} border rounded-full px-3 py-1 text-xs font-medium`}>
              {task.priority}
            </Badge>
          )}

          {task.tags && task.tags.length > 0 && (
            <div className="flex gap-1">
              {task.tags.map((tag, index) => (
                <Badge key={index} variant="secondary" className="rounded-full px-2 py-1 text-xs">
                  {tag}
                </Badge>
              ))}
            </div>
          )}

          {task.due_date && (
            <span className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded">
              Due: {new Date(task.due_date).toLocaleDateString()}
            </span>
          )}
        </div>
      </div>

      <div className="flex gap-1 flex-shrink-0">
        <Button
          variant="outline"
          size="sm"
          onClick={() => setIsEditing(!isEditing)}
          className="h-8 w-8 p-0"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/>
          </svg>
        </Button>
        <Button
          variant="outline"
          size="sm"
          onClick={handleDeleteClick}
          className="h-8 w-8 p-0 text-destructive hover:text-destructive"
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