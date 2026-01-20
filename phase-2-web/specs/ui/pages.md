# UI Pages Specification

## Pages Overview

This document defines all pages and routes for the Phase II Todo App frontend using Next.js 16+ App Router.

---

## Route Structure

```
/                           → Redirect to /login or /dashboard
/login                      → Login page
/signup                     → Signup page
/dashboard                  → Main dashboard (protected)
/dashboard/tasks            → Task list (default dashboard view)
/dashboard/tasks/new        → Create new task (modal)
/dashboard/tasks/[id]       → Task detail page
```

---

## Page Routes

### 1. Root Redirect

**Route:** `/`

**Purpose:** Redirect based on authentication status

**Implementation:**
```tsx
// app/page.tsx
import { redirect } from 'next/navigation';
import { auth } from '@/lib/auth';

export default async function RootPage() {
  const session = await auth();

  if (session) {
    redirect('/dashboard');
  } else {
    redirect('/login');
  }
}
```

---

### 2. Login Page

**Route:** `/login`

**Purpose:** User authentication

**File:** `app/(auth)/login/page.tsx`

**Components:**
- Header with logo
- LoginForm component
- "Don't have an account? Sign up" link

**Layout:**
```tsx
// app/(auth)/layout.tsx
export default function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full">
        {/* Logo */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Todo App</h1>
          <p className="text-gray-500 mt-2">Manage your tasks efficiently</p>
        </div>
        {children}
      </div>
    </div>
  );
}
```

**Page Implementation:**
```tsx
// app/(auth)/login/page.tsx
import { LoginForm } from '@/components/forms/login-form';
import Link from 'next/link';

export default function LoginPage() {
  return (
    <div className="bg-white rounded-lg shadow-md p-8">
      <h2 className="text-2xl font-semibold mb-6">Welcome back</h2>
      <LoginForm />
      <p className="text-center mt-6 text-sm text-gray-600">
        Don't have an account?{' '}
        <Link href="/signup" className="text-blue-600 hover:underline">
          Sign up
        </Link>
      </p>
    </div>
  );
}
```

**State Management:**
```tsx
// components/forms/login-form.tsx
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { api } from '@/lib/api';

export function LoginForm() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await api.login({ email, password });
      if (response.success) {
        router.push('/dashboard');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-lg">
          {error}
        </div>
      )}

      <div>
        <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
          Email
        </label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          placeholder="you@example.com"
        />
      </div>

      <div>
        <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
          Password
        </label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          minLength={8}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          placeholder="••••••••"
        />
      </div>

      <button
        type="submit"
        disabled={loading}
        className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
      >
        {loading ? 'Logging in...' : 'Log in'}
      </button>
    </form>
  );
}
```

---

### 3. Signup Page

**Route:** `/signup`

**Purpose:** New user registration

**File:** `app/(auth)/signup/page.tsx`

**Components:**
- Header with logo
- SignupForm component
- "Already have an account? Login" link

**Page Implementation:**
```tsx
// app/(auth)/signup/page.tsx
import { SignupForm } from '@/components/forms/signup-form';
import Link from 'next/link';

export default function SignupPage() {
  return (
    <div className="bg-white rounded-lg shadow-md p-8">
      <h2 className="text-2xl font-semibold mb-6">Create account</h2>
      <SignupForm />
      <p className="text-center mt-6 text-sm text-gray-600">
        Already have an account?{' '}
        <Link href="/login" className="text-blue-600 hover:underline">
          Log in
        </Link>
      </p>
    </div>
  );
}
```

**SignupForm Component:**
```tsx
// components/forms/signup-form.tsx
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { api } from '@/lib/api';

export function SignupForm() {
  const router = useRouter();
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    setLoading(true);

    try {
      const response = await api.signup({ name, email, password });
      if (response.success) {
        api.setToken(response.data.token);
        router.push('/dashboard');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Signup failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-lg">
          {error}
        </div>
      )}

      <div>
        <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">
          Name <span className="text-gray-400">(optional)</span>
        </label>
        <input
          id="name"
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          maxLength={100}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          placeholder="John Doe"
        />
      </div>

      <div>
        <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
          Email
        </label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          placeholder="you@example.com"
        />
      </div>

      <div>
        <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
          Password
        </label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          minLength={8}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          placeholder="••••••••"
        />
        <p className="text-xs text-gray-500 mt-1">Must be at least 8 characters</p>
      </div>

      <div>
        <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700 mb-1">
          Confirm Password
        </label>
        <input
          id="confirmPassword"
          type="password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          required
          minLength={8}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          placeholder="••••••••"
        />
      </div>

      <button
        type="submit"
        disabled={loading}
        className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
      >
        {loading ? 'Creating account...' : 'Sign up'}
      </button>
    </form>
  );
}
```

---

### 4. Dashboard Page

**Route:** `/dashboard`

**Purpose:** Main task management interface

**File:** `app/dashboard/page.tsx`

**Protection:** Requires authentication (redirect to `/login` if not authenticated)

**Layout:**
```tsx
// app/dashboard/layout.tsx
import { auth } from '@/lib/auth';
import { redirect } from 'next/navigation';

export default async function DashboardLayout({
  children
}: {
  children: React.ReactNode
}) {
  const session = await auth();

  if (!session) {
    redirect('/login');
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <h1 className="text-xl font-bold text-gray-900">Todo App</h1>
            <UserMenu />
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>
    </div>
  );
}
```

**Dashboard Page Implementation:**
```tsx
// app/dashboard/page.tsx
import { TaskList } from '@/components/tasks/task-list';
import { TaskFormModal } from '@/components/tasks/task-form-modal';
import { api } from '@/lib/api';

export default async function DashboardPage() {
  // Fetch tasks server-side
  const tasks = await api.getTasks({ limit: 20 });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">My Tasks</h2>
          <p className="text-gray-500">Manage your to-do items</p>
        </div>
        <TaskFormModal>
          <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 font-medium">
            + New Task
          </button>
        </TaskFormModal>
      </div>

      {/* Task List */}
      <TaskList tasks={tasks.data.tasks} />
    </div>
  );
}
```

**TaskFormModal Component:**
```tsx
// components/tasks/task-form-modal.tsx
'use client';

import { useState } from 'react';
import { Modal } from '@/components/ui/modal';
import { TaskForm } from './task-form';
import { api } from '@/lib/api';

interface TaskFormModalProps {
  children: React.ReactNode;
}

export function TaskFormModal({ children }: TaskFormModalProps) {
  const [isOpen, setIsOpen] = useState(false);

  const handleSubmit = async (data: { title: string; description?: string }) => {
    await api.createTask(data);
    setIsOpen(false);
    // Refresh the page to show new task
    window.location.reload();
  };

  return (
    <>
      <div onClick={() => setIsOpen(true)}>
        {children}
      </div>

      <Modal isOpen={isOpen} onClose={() => setIsOpen(false)} title="Create Task">
        <TaskForm onSubmit={handleSubmit} onCancel={() => setIsOpen(false)} />
      </Modal>
    </>
  );
}
```

---

### 5. Task Detail Page

**Route:** `/dashboard/tasks/[id]`

**Purpose:** View and edit single task

**File:** `app/dashboard/tasks/[id]/page.tsx`

**Protection:** Requires authentication

**Implementation:**
```tsx
// app/dashboard/tasks/[id]/page.tsx
import { notFound } from 'next/navigation';
import { TaskDetail } from '@/components/tasks/task-detail';
import { api } from '@/lib/api';

export default async function TaskDetailPage({ params }: { params: { id: string } }) {
  try {
    const response = await api.getTask(parseInt(params.id));
    const task = response.data;

    return (
      <div className="max-w-2xl mx-auto">
        <TaskDetail task={task} />
      </div>
    );
  } catch (error) {
    notFound();
  }
}
```

**TaskDetail Component:**
```tsx
// components/tasks/task-detail.tsx
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Task } from '@/types/task';
import { api } from '@/lib/api';
import { TaskFormModal } from './task-form-modal';

interface TaskDetailProps {
  task: Task;
}

export function TaskDetail({ task }: TaskDetailProps) {
  const router = useRouter();
  const [isEditing, setIsEditing] = useState(false);

  const handleDelete = async () => {
    if (confirm('Are you sure you want to delete this task?')) {
      await api.deleteTask(task.id);
      router.push('/dashboard');
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      {/* Header */}
      <div className="flex justify-between items-start mb-6">
        <h1 className="text-2xl font-bold">{task.title}</h1>
        <div className="flex gap-2">
          <button
            onClick={() => setIsEditing(true)}
            className="px-3 py-2 text-sm bg-gray-100 rounded-lg hover:bg-gray-200"
          >
            Edit
          </button>
          <button
            onClick={handleDelete}
            className="px-3 py-2 text-sm bg-red-100 text-red-600 rounded-lg hover:bg-red-200"
          >
            Delete
          </button>
        </div>
      </div>

      {/* Content */}
      {task.description && (
        <div className="mb-6">
          <h3 className="text-sm font-medium text-gray-500 mb-2">Description</h3>
          <p className="text-gray-700 whitespace-pre-wrap">{task.description}</p>
        </div>
      )}

      {/* Metadata */}
      <div className="text-sm text-gray-500 space-y-1">
        <p>Status: {task.completed ? '✅ Completed' : '⏳ Pending'}</p>
        <p>Created: {new Date(task.created_at).toLocaleString()}</p>
        <p>Updated: {new Date(task.updated_at).toLocaleString()}</p>
      </div>

      {/* Edit Modal */}
      {isEditing && (
        <TaskFormModal task={task}>
          <div />
        </TaskFormModal>
      )}

      {/* Back Button */}
      <button
        onClick={() => router.push('/dashboard')}
        className="mt-6 text-blue-600 hover:underline"
      >
        ← Back to tasks
      </button>
    </div>
  );
}
```

---

## Shared Components

### Header Component

**Location:** `components/layout/header.tsx`

```tsx
'use client';

import Link from 'next/link';
import { auth } from '@/lib/auth';

export async function Header() {
  const session = await auth();

  return (
    <header className="bg-white border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <Link href="/" className="text-xl font-bold text-gray-900">
            Todo App
          </Link>

          <nav className="flex items-center gap-4">
            {session ? (
              <>
                <Link
                  href="/dashboard"
                  className="text-gray-700 hover:text-gray-900"
                >
                  Dashboard
                </Link>
                <form action="/api/auth/signout" method="POST">
                  <button
                    type="submit"
                    className="text-gray-700 hover:text-gray-900"
                  >
                    Sign out
                  </button>
                </form>
              </>
            ) : (
              <>
                <Link
                  href="/login"
                  className="text-gray-700 hover:text-gray-900"
                >
                  Log in
                </Link>
                <Link
                  href="/signup"
                  className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
                >
                  Sign up
                </Link>
              </>
            )}
          </nav>
        </div>
      </div>
    </header>
  );
}
```

---

## Protected Route Pattern

**Middleware for Authentication:**

```tsx
// middleware.ts
import { auth } from '@/lib/auth';
import { NextResponse } from 'next/server';

export default auth((req) => {
  const isAuthenticated = !!req.auth;
  const isOnDashboard = req.nextUrl.pathname.startsWith('/dashboard');

  if (isOnDashboard && !isAuthenticated) {
    return NextResponse.redirect(new URL('/login', req.url));
  }

  if ((req.nextUrl.pathname === '/login' || req.nextUrl.pathname === '/signup') && isAuthenticated) {
    return NextResponse.redirect(new URL('/dashboard', req.url));
  }
});

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)']
};
```

---

## Error Handling

### not-found.tsx

```tsx
// app/not-found.tsx
import Link from 'next/link';

export default function NotFound() {
  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-center">
        <h1 className="text-6xl font-bold text-gray-900 mb-4">404</h1>
        <p className="text-xl text-gray-600 mb-8">Page not found</p>
        <Link
          href="/"
          className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700"
        >
          Go home
        </Link>
      </div>
    </div>
  );
}
```

### error.tsx

```tsx
// app/error.tsx
'use client';

import { useEffect } from 'react';

export default function Error({
  error,
  reset
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error(error);
  }, [error]);

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-center">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Something went wrong!</h2>
        <button
          onClick={reset}
          className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700"
        >
          Try again
        </button>
      </div>
    </div>
  );
}
```

---

## Loading States

### loading.tsx

```tsx
// app/dashboard/loading.tsx
export default function DashboardLoading() {
  return (
    <div className="space-y-6">
      <div className="animate-pulse bg-gray-200 h-8 rounded w-1/4" />
      <div className="space-y-4">
        {[1, 2, 3].map((i) => (
          <div key={i} className="animate-pulse bg-gray-200 h-20 rounded-lg" />
        ))}
      </div>
    </div>
  );
}
```

---

## Related Specifications

- **Overview:** `@specs/overview.md`
- **Architecture:** `@specs/architecture.md`
- **Features:** `@specs/features/`
- **API:** `@specs/api/rest-endpoints.md`
- **Database:** `@specs/database/schema.md`
- **Components:** `@specs/ui/components.md`

---

**Document Status:** ✅ Ready for Review
**Last Updated:** January 17, 2026
**Phase:** Phase II - Full-Stack Web Application
