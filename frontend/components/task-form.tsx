'use client';

/**
 * TaskForm with Custom Color Palette
 * #092635, #1B4242, #5C8374, #9EC8B9
 */

import { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { taskCreateSchema, type TaskCreateFormData } from '@/lib/validation';
import { Task, TaskCreate, TaskUpdate } from '@/lib/types';
import { createTask, updateTask } from '@/lib/tasks';

interface TaskFormProps {
  onSuccess: () => void;
  editTask?: Task | null;
  onCancelEdit?: () => void;
}

export default function TaskForm({ onSuccess, editTask, onCancelEdit }: TaskFormProps) {
  const isEditing = !!editTask;
  const [error, setError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    reset,
  } = useForm<TaskCreateFormData>({
    resolver: zodResolver(taskCreateSchema),
    defaultValues: {
      title: '',
      description: '',
      priority: 'medium',
      due_date: '',
      category: '',
    },
  });

  useEffect(() => {
    if (editTask) {
      reset({
        title: editTask.title,
        description: editTask.description || '',
        priority: editTask.priority || 'medium',
        due_date: editTask.due_date || '',
        category: editTask.category || '',
      });
    }
  }, [editTask, reset]);

  const onSubmit = async (data: TaskCreateFormData) => {
    setError(null);
    try {
      if (isEditing && editTask) {
        const updateData: TaskUpdate = {
          title: data.title,
          description: data.description || undefined,
          priority: data.priority || 'medium',
          due_date: data.due_date || undefined,
          category: data.category || undefined,
        };
        await updateTask(editTask.id, updateData);
        onCancelEdit?.();
      } else {
        const newTask: TaskCreate = {
          title: data.title,
          description: data.description || undefined,
          priority: data.priority || 'medium',
          due_date: data.due_date || undefined,
          category: data.category || undefined,
        };
        await createTask(newTask);
        reset();
      }
      onSuccess();
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to save task';
      setError(message);
    }
  };

  const handleCancel = () => {
    reset();
    onCancelEdit?.();
  };

  return (
    <div className="group relative">
      {/* Glow effect */}
      <div className="absolute inset-0 rounded-3xl blur-xl opacity-30 group-hover:opacity-50 transition-opacity duration-300" style={{ background: 'linear-gradient(to right, #5C8374, #9EC8B9)' }}></div>

      <div className="relative backdrop-blur-xl bg-white/5 rounded-3xl border border-white/10 overflow-hidden">
        {/* Header with gradient */}
        <div className="relative overflow-hidden">
          <div className="absolute inset-0" style={{ background: 'linear-gradient(to right, #5C8374, #9EC8B9)' }}></div>
          <div className="relative px-6 py-5">
            <div className="flex items-center space-x-3">
              <div className="relative">
                <div className="absolute inset-0 bg-white/20 rounded-xl blur-sm"></div>
                <div className="relative p-2 bg-white/10 rounded-xl backdrop-blur-sm">
                  <svg className="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                </div>
              </div>
              <h3 className="text-xl font-bold text-white">
                {isEditing ? '✏️ Edit Task' : '✨ Create New Task'}
              </h3>
            </div>
          </div>
        </div>

        <div className="p-6">
          {error && (
            <div className="mb-5 relative">
              <div className="absolute inset-0 rounded-2xl blur-md" style={{ background: '#1B4242' }}></div>
              <div className="relative bg-white/10 border border-white/20 text-white px-4 py-3 rounded-2xl flex items-center justify-between">
                <div className="flex items-center">
                  <svg className="w-5 h-5 mr-2 text-red-400" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                  </svg>
                  <span className="text-sm font-medium">{error}</span>
                </div>
                <button
                  onClick={() => setError(null)}
                  className="p-1 hover:bg-white/20 rounded-lg transition-colors"
                >
                  <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l-4.293 4.293a1 1 0 010-1.414z" clipRule="evenodd" />
                  </svg>
                </button>
              </div>
            </div>
          )}

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
            {/* Title Field */}
            <div>
              <label htmlFor="title" className="block text-sm font-medium text-white/80 mb-2 flex items-center">
                <span className="mr-2">📌</span>
                Title <span className="text-red-400">*</span>
              </label>
              <input
                {...register('title')}
                type="text"
                id="title"
                className="block w-full rounded-2xl border-2 border-white/20 bg-white/5 backdrop-blur-sm focus:border-white/30 focus:outline-none sm:text-sm px-4 py-3 transition-all duration-200 placeholder-white/40"
                placeholder="What needs to be done? ✨"
              />
              {errors.title && (
                <p className="mt-2 text-sm text-red-400">{errors.title.message}</p>
              )}
            </div>

            {/* Description Field */}
            <div>
              <label htmlFor="description" className="block text-sm font-medium text-white/80 mb-2 flex items-center">
                <span className="mr-2">📝</span>
                Description
              </label>
              <textarea
                {...register('description')}
                id="description"
                rows={3}
                className="block w-full rounded-2xl border-2 border-white/20 bg-white/5 backdrop-blur-sm focus:border-white/30 focus:outline-none sm:text-sm px-4 py-3 transition-all duration-200 placeholder-white/40 resize-none"
                placeholder="Add more details (optional) 💡"
              />
              {errors.description && (
                <p className="mt-2 text-sm text-red-400">{errors.description.message}</p>
              )}
            </div>

            {/* Priority, Due Date, Category - 3 Columns */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {/* Priority */}
              <div>
                <label htmlFor="priority" className="block text-sm font-medium text-white/80 mb-2 flex items-center">
                  <span className="mr-2">⭐</span>
                  Priority
                </label>
                <select
                  {...register('priority')}
                  id="priority"
                  className="block w-full rounded-2xl border-2 border-white/20 bg-white/5 backdrop-blur-sm focus:border-white/30 focus:outline-none sm:text-sm px-4 py-3 transition-all duration-200 text-white"
                >
                  <option value="low" className="bg-gray-800">🟢 Low</option>
                  <option value="medium" className="bg-gray-800">🟡 Medium</option>
                  <option value="high" className="bg-gray-800">🔴 High</option>
                </select>
                {errors.priority && (
                  <p className="mt-2 text-sm text-red-400">{errors.priority.message}</p>
                )}
              </div>

              {/* Due Date */}
              <div>
                <label htmlFor="due_date" className="block text-sm font-medium text-white/80 mb-2 flex items-center">
                  <span className="mr-2">📅</span>
                  Due Date
                </label>
                <input
                  {...register('due_date')}
                  type="date"
                  id="due_date"
                  className="block w-full rounded-2xl border-2 border-white/20 bg-white/5 backdrop-blur-sm focus:border-white/30 focus:outline-none sm:text-sm px-4 py-3 transition-all duration-200 text-white [color-scheme:dark]"
                />
                {errors.due_date && (
                  <p className="mt-2 text-sm text-red-400">{errors.due_date.message}</p>
                )}
              </div>

              {/* Category */}
              <div>
                <label htmlFor="category" className="block text-sm font-medium text-white/80 mb-2 flex items-center">
                  <span className="mr-2">🏷️</span>
                  Category
                </label>
                <input
                  {...register('category')}
                  type="text"
                  id="category"
                  className="block w-full rounded-2xl border-2 border-white/20 bg-white/5 backdrop-blur-sm focus:border-white/30 focus:outline-none sm:text-sm px-4 py-3 transition-all duration-200 placeholder-white/40"
                  placeholder="e.g., Work, Personal"
                />
                {errors.category && (
                  <p className="mt-2 text-sm text-red-400">{errors.category.message}</p>
                )}
              </div>
            </div>

            {/* Actions */}
            <div className="flex justify-end space-x-3 pt-4">
              {isEditing && (
                <button
                  type="button"
                  onClick={handleCancel}
                  className="px-6 py-3 border-2 border-white/20 rounded-2xl text-sm font-semibold text-white/80 bg-white/5 backdrop-blur-sm hover:bg-white/10 focus:outline-none transition-all duration-200 hover:scale-105"
                >
                  Cancel
                </button>
              )}
              <button
                type="submit"
                disabled={isSubmitting}
                className="group relative px-8 py-3 rounded-2xl text-sm font-semibold text-white overflow-hidden transition-all duration-300 hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed"
                style={{ background: 'linear-gradient(to right, #5C8374, #9EC8B9)' }}
              >
                <span className="relative flex items-center">
                  {isSubmitting ? (
                    <>
                      <svg className="animate-spin -ml-1 mr-2 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      Saving...
                    </>
                  ) : (
                    <span className="flex items-center">
                      {isEditing ? (
                        <>
                          <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l4 4m4-4h1m-4 0v1a3 3 0 003 3h10a3 3 0 003-3v-1" />
                          </svg>
                          Update Task
                        </>
                      ) : (
                        <>
                          <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                          </svg>
                          Create Task
                        </>
                      )}
                    </span>
                  )}
                </span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
