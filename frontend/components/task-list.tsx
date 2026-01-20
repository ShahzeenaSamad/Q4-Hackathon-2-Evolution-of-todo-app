'use client';

/**
 * Unique Colorful TaskList Component with Animations
 *
 * Displays a list of tasks with beautiful colorful card design
 */

import { useState } from 'react';
import { Task } from '@/lib/types';
import { deleteTask, toggleTaskComplete } from '@/lib/tasks';

interface TaskListProps {
  tasks: Task[];
  onTasksChange: () => void;
  onEditTask: (task: Task) => void;
}

export default function TaskList({ tasks, onTasksChange, onEditTask }: TaskListProps) {
  const [deletingId, setDeletingId] = useState<number | null>(null);
  const [togglingId, setTogglingId] = useState<number | null>(null);

  const handleToggleComplete = async (taskId: number) => {
    setTogglingId(taskId);
    try {
      await toggleTaskComplete(taskId);
      onTasksChange();
    } catch (error) {
      alert(error instanceof Error ? error.message : 'Failed to toggle task');
    } finally {
      setTogglingId(null);
    }
  };

  const handleDelete = async (taskId: number) => {
    if (!confirm('Are you sure you want to delete this task?')) {
      return;
    }

    setDeletingId(taskId);
    try {
      await deleteTask(taskId);
      onTasksChange();
    } catch (error) {
      alert(error instanceof Error ? error.message : 'Failed to delete task');
    } finally {
      setDeletingId(null);
    }
  };

  if (tasks.length === 0) {
    return null;
  }

  return (
    <div className="space-y-4">
      {tasks.map((task, index) => (
        <div
          key={task.id}
          className="group relative"
          style={{
            animation: `slideIn 0.5s ease-out ${index * 0.1}s both`
          }}
        >
          {/* Glow effect */}
          <div className={`absolute inset-0 rounded-3xl blur-xl transition-opacity duration-300 ${
            task.completed
              ? 'bg-gradient-to-r from-green-400 to-emerald-400 opacity-40'
              : 'bg-gradient-to-r from-pink-400 via-purple-400 to-indigo-400 opacity-20'
          } group-hover:opacity-40`}></div>

          {/* Card */}
          <div className={`relative backdrop-blur-xl rounded-3xl p-6 border-2 transition-all duration-300 hover:scale-[1.02] hover:shadow-2xl ${
            task.completed
              ? 'bg-gradient-to-br from-green-50/50 to-emerald-50/50 border-green-300/50'
              : 'bg-gradient-to-br from-white/60 to-purple-50/60 border-purple-200/50'
          }`}>
            <div className="flex items-start justify-between gap-4">
              {/* Checkbox and Content */}
              <div className="flex items-start gap-4 flex-1">
                <button
                  onClick={() => handleToggleComplete(task.id)}
                  disabled={togglingId === task.id}
                  className={`mt-1 flex-shrink-0 w-9 h-9 rounded-2xl border-2 flex items-center justify-center transition-all duration-200 ${
                    task.completed
                      ? 'bg-gradient-to-br from-green-400 to-emerald-500 border-green-400 shadow-lg scale-100'
                      : 'bg-gradient-to-br from-pink-100 to-purple-100 border-pink-300 hover:border-pink-400 hover:scale-110'
                  } ${togglingId === task.id ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}
                >
                  {task.completed ? (
                    <svg className="w-6 h-6 text-white animate-bounce-in" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                    </svg>
                  ) : (
                    <div className="w-5 h-5 rounded-full border-2 border-purple-400"></div>
                  )}
                </button>

                <div className="flex-1 min-w-0">
                  <h4
                    className={`font-bold text-xl mb-2 transition-all duration-200 ${
                      task.completed
                        ? 'text-green-700 line-through decoration-3 decoration-green-400'
                        : 'text-gray-900 group-hover:text-transparent group-hover:bg-clip-text group-hover:bg-gradient-to-r group-hover:from-pink-600 group-hover:to-purple-600'
                    }`}
                  >
                    {task.title}
                  </h4>

                  {/* Priority, Category, Due Date badges */}
                  <div className="flex flex-wrap items-center gap-2 mb-3">
                    {/* Priority Badge */}
                    {task.priority && (
                      <span
                        className={`inline-flex items-center text-xs font-semibold px-3 py-1 rounded-full border-2 shadow-sm ${
                          task.priority === 'high'
                            ? 'text-red-700 bg-red-100/80 border-red-300'
                            : task.priority === 'medium'
                            ? 'text-amber-700 bg-amber-100/80 border-amber-300'
                            : 'text-green-700 bg-green-100/80 border-green-300'
                        }`}
                      >
                        {task.priority === 'high' ? '🔴' : task.priority === 'medium' ? '🟡' : '🟢'} {task.priority.charAt(0).toUpperCase() + task.priority.slice(1)}
                      </span>
                    )}

                    {/* Category Badge */}
                    {task.category && (
                      <span className="inline-flex items-center text-xs font-semibold text-purple-700 bg-purple-100/80 backdrop-blur-sm px-3 py-1 rounded-full border-2 border-purple-300 shadow-sm">
                        🏷️ {task.category}
                      </span>
                    )}

                    {/* Due Date Badge */}
                    {task.due_date && (
                      <span className="inline-flex items-center text-xs font-semibold text-blue-700 bg-blue-100/80 backdrop-blur-sm px-3 py-1 rounded-full border-2 border-blue-300 shadow-sm">
                        📅 {new Date(task.due_date).toLocaleDateString('en-US', {
                          month: 'short',
                          day: 'numeric'
                        })}
                        {new Date(task.due_date) < new Date() && !task.completed && (
                          <span className="ml-1 text-red-600">⚠️</span>
                        )}
                      </span>
                    )}
                  </div>

                  {task.description && (
                    <p
                      className={`mt-2 text-base leading-relaxed transition-all duration-200 ${
                        task.completed
                          ? 'text-green-600 line-through decoration-2 decoration-green-400 opacity-75'
                          : 'text-gray-600'
                      }`}
                    >
                      {task.description}
                    </p>
                  )}
                  <div className="mt-4 flex items-center gap-3">
                    <span className="inline-flex items-center text-xs text-purple-700 bg-white/60 backdrop-blur-sm px-3 py-1.5 rounded-full border border-purple-200 shadow-sm">
                      <svg className="w-3.5 h-3.5 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                      </svg>
                      {new Date(task.created_at).toLocaleDateString('en-US', {
                        month: 'short',
                        day: 'numeric',
                        year: 'numeric'
                      })}
                    </span>
                    {task.completed && (
                      <span className="inline-flex items-center text-xs text-green-700 bg-green-100/80 backdrop-blur-sm px-3 py-1.5 rounded-full border-2 border-green-300 shadow-sm animate-pulse">
                        <svg className="w-3.5 h-3.5 mr-1.5" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                        </svg>
                        Completed!
                      </span>
                    )}
                  </div>
                </div>
              </div>

              {/* Actions */}
              <div className="flex items-center gap-2 flex-shrink-0 opacity-0 group-hover:opacity-100 transition-all duration-300 transform translate-x-2 group-hover:translate-x-0">
                <button
                  onClick={() => onEditTask(task)}
                  className="p-3 text-purple-400 hover:text-pink-600 hover:bg-pink-50 rounded-2xl transition-all duration-200 hover:scale-110"
                  title="Edit task"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                </button>
                <button
                  onClick={() => handleDelete(task.id)}
                  disabled={deletingId === task.id}
                  className="p-3 text-purple-400 hover:text-red-600 hover:bg-red-50 rounded-2xl transition-all duration-200 hover:scale-110"
                  title="Delete task"
                >
                  {deletingId === task.id ? (
                    <svg className="animate-spin w-6 h-6 text-red-600" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                    </svg>
                  ) : (
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  )}
                </button>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
