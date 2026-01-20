/**
 * Validation schemas using Zod.
 *
 * Provides form validation that matches backend rules exactly.
 */

import { z } from 'zod';

/**
 * Password validation rules (matches backend):
 * - Minimum 8 characters
 * - At least one lowercase letter
 * - At least one uppercase letter
 * - At least one digit
 * - At least one special character
 */
const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]).{8,}$/;

/**
 * Signup form validation schema
 */
export const signupSchema = z.object({
  email: z
    .string()
    .min(1, 'Email is required')
    .email('Invalid email address')
    .toLowerCase()
    .trim(),
  password: z
    .string()
    .min(1, 'Password is required')
    .min(8, 'Password must be at least 8 characters long')
    .regex(
      passwordRegex,
      'Password must contain uppercase, lowercase, digit, and special character'
    ),
  confirmPassword: z
    .string()
    .min(1, 'Please confirm your password'),
  name: z
    .string()
    .max(100, 'Name must be less than 100 characters')
    .optional()
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ['confirmPassword'],
});

export type SignupFormData = z.infer<typeof signupSchema>;

/**
 * Login form validation schema
 */
export const loginSchema = z.object({
  email: z
    .string()
    .min(1, 'Email is required')
    .email('Invalid email address')
    .toLowerCase()
    .trim(),
  password: z
    .string()
    .min(1, 'Password is required'),
});

export type LoginFormData = z.infer<typeof loginSchema>;

/**
 * Task creation validation schema
 */
export const taskCreateSchema = z.object({
  title: z
    .string()
    .min(1, 'Title is required')
    .max(200, 'Title must be less than 200 characters')
    .refine((val) => val.trim().length > 0, {
      message: 'Title cannot be empty or whitespace only',
    }),
  description: z
    .string()
    .max(1000, 'Description must be less than 1000 characters')
    .optional()
    .nullable(),
  priority: z
    .enum(['low', 'medium', 'high'], {
      errorMap: () => ({ message: 'Priority must be low, medium, or high' })
    })
    .default('medium'),
  due_date: z
    .string()
    .optional()
    .nullable(),
  category: z
    .string()
    .max(50, 'Category must be less than 50 characters')
    .optional()
    .nullable(),
});

export type TaskCreateFormData = z.infer<typeof taskCreateSchema>;

/**
 * Task update validation schema
 */
export const taskUpdateSchema = z.object({
  title: z
    .string()
    .min(1, 'Title is required')
    .max(200, 'Title must be less than 200 characters')
    .refine((val) => val.trim().length > 0, {
      message: 'Title cannot be empty or whitespace only',
    })
    .optional()
    .nullable(),
  description: z
    .string()
    .max(1000, 'Description must be less than 1000 characters')
    .optional()
    .nullable(),
  priority: z
    .enum(['low', 'medium', 'high'])
    .optional()
    .nullable(),
  due_date: z
    .string()
    .optional()
    .nullable(),
  category: z
    .string()
    .max(50, 'Category must be less than 50 characters')
    .optional()
    .nullable(),
});

export type TaskUpdateFormData = z.infer<typeof taskUpdateSchema>;
