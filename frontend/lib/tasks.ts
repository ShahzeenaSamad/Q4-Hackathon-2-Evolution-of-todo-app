/**
 * Task API functions
 * Handles all task-related API calls
 */

import { apiRequest } from './auth';
import { Task, TaskCreate, TaskUpdate } from './types';

/**
 * Get all tasks for the authenticated user
 */
export async function getTasks(): Promise<Task[]> {
  const response = await apiRequest('/api/v1/tasks/');

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to fetch tasks');
  }

  const data = await response.json();
  return data.data;
}

/**
 * Get a single task by ID
 */
export async function getTask(taskId: number): Promise<Task> {
  const response = await apiRequest(`/api/v1/tasks/${taskId}`);

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to fetch task');
  }

  const data = await response.json();
  return data.data;
}

/**
 * Create a new task
 */
export async function createTask(taskData: TaskCreate): Promise<Task> {
  const response = await apiRequest(`/api/v1/tasks/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(taskData),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to create task');
  }

  const data = await response.json();
  return data.data;
}

/**
 * Update an existing task
 */
export async function updateTask(taskId: number, taskData: TaskUpdate): Promise<Task> {
  const response = await apiRequest(`/api/v1/tasks/${taskId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(taskData),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to update task');
  }

  const data = await response.json();
  return data.data;
}

/**
 * Toggle task completion status
 */
export async function toggleTaskComplete(taskId: number): Promise<Task> {
  const response = await apiRequest(`/api/v1/tasks/${taskId}/complete`, {
    method: 'PATCH',
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to toggle task');
  }

  const data = await response.json();
  return data.data;
}

/**
 * Delete a task
 */
export async function deleteTask(taskId: number): Promise<void> {
  const response = await apiRequest(`/api/v1/tasks/${taskId}`, {
    method: 'DELETE',
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to delete task');
  }
}
