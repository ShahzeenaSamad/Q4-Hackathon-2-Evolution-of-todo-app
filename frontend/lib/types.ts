/**
 * Shared TypeScript types for Todo App
 * These types must match the backend SQLModel definitions
 */

/**
 * User entity type
 * Matches backend User model in backend/models/user.py
 */
export interface User {
  id: string;
  email: string;
  name: string | null;
  created_at: Date;
}

/**
 * Task entity type
 * Matches backend Task model in backend/models/task.py
 */
export interface Task {
  id: number;
  user_id: string;
  title: string;
  description: string | null;
  completed: boolean;
  priority: 'low' | 'medium' | 'high';
  due_date: string | null;
  category: string | null;
  created_at: Date;
  updated_at: Date;
}

/**
 * Create Task request type
 * Used when creating a new task
 */
export interface TaskCreate {
  title: string;
  description?: string;
  priority?: 'low' | 'medium' | 'high';
  due_date?: string;
  category?: string;
}

/**
 * Update Task request type
 * Used when updating an existing task
 */
export interface TaskUpdate {
  title?: string;
  description?: string;
  completed?: boolean;
  priority?: 'low' | 'medium' | 'high';
  due_date?: string;
  category?: string;
}

/**
 * Auth response types
 */
export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in?: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface SignupRequest {
  email: string;
  password: string;
  name?: string;
}

export interface AuthResponse {
  success: boolean;
  data: {
    user: User;
    tokens: AuthTokens;
  } | null;
  error: {
    code: string;
    message: string;
  } | null;
}

/**
 * API Error response type
 */
export interface ApiError {
  success: false;
  error: {
    code: string;
    message: string;
    details?: Record<string, unknown>;
  };
}

/**
 * Task Statistics type
 */
export interface TaskStatistics {
  total: number;
  completed: number;
  pending: number;
}
