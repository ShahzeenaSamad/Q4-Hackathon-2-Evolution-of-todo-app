# Skill: Next.js Frontend Builder

## Metadata

**Skill Name:** `nextjs-frontend`

**Description:** Build Next.js App Router applications with authentication, API integration, reusable components, and responsive UI.

**Version:** 1.0

**Author:** Claude Code

**Created:** January 17, 2026

---

## Purpose

This skill implements modern, production-ready Next.js 16+ frontend applications following:
- App Router architecture
- Server and client components
- Better Auth integration
- API client integration
- Responsive design with Tailwind CSS
- TypeScript for type safety
- Reusable component library

---

## When to Use

Use this skill when:
- Implementing Next.js 16+ frontend applications
- Creating React components and pages
- Integrating authentication (Better Auth)
- Building API clients
- Designing responsive UI layouts
- Setting up routing and navigation
- Creating forms and user interactions

**Prerequisites:**
- Node.js 18+ installed
- Next.js 16+ concepts understood
- Backend API endpoints specified
- UI/UX specifications approved

---

## Core Principles

1. **App Router First:** Use Next.js 16+ App Router (not Pages Router)
2. **Server Components Default:** Use server components by default, client components only when needed
3. **TypeScript Always:** All components must have TypeScript
4. **Authentication First:** Protected routes require authentication
5. **API Integration:** Centralized API client for all backend calls
6. **Responsive Design:** Mobile-first approach with Tailwind CSS

---

## Project Structure

```
frontend/
├── app/                      # App Router directory
│   ├── (auth)/              # Auth route group
│   │   ├── login/
│   │   └── signup/
│   ├── dashboard/           # Protected routes
│   │   └── tasks/
│   ├── layout.tsx           # Root layout
│   └── page.tsx             # Home page
├── components/
│   ├── ui/                  # Reusable UI components
│   │   ├── button.tsx
│   │   ├── input.tsx
│   │   └── card.tsx
│   ├── forms/               # Form components
│   │   ├── login-form.tsx
│   │   └── task-form.tsx
│   └── tasks/               # Task-specific components
│       ├── task-list.tsx
│       ├── task-card.tsx
│       └── task-form-modal.tsx
├── lib/
│   ├── api.ts               # API client
│   ├── auth.ts              # Auth utilities
│   └── utils.ts            # Helper functions
├── styles/                  # Global styles
├── public/                  # Static assets
├── package.json            # Dependencies
└── tsconfig.json           # TypeScript config
```

---

## Implementation Patterns

### 1. App Router Page Structure

**Server Component (Default):**
```tsx
// app/dashboard/page.tsx
import { TaskList } from '@/components/tasks/task-list'

export default async function DashboardPage() {
  // Server-side data fetching
  const response = await fetch('http://localhost:8000/api/v1/tasks', {
    headers: {
      'Authorization': `Bearer ${await getToken()}`
    }
  })
  const { data } = await response.json()

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold">My Tasks</h1>
      <TaskList tasks={data.tasks} />
    </div>
  )
}
```

**Client Component (When Needed):**
```tsx
'use client'

import { useState } from 'react'

export function TaskFormModal() {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <div>
      <button onClick={() => setIsOpen(true)}>Open</button>
      {isOpen && <Modal onClose={() => setIsOpen(false)} />}
    </div>
  )
}
```

**Rules:**
- ✅ Use `'use client'` directive only for interactive components
- ✅ Server components by default (better performance)
- ✅ Client components for: forms, modals, interactivity
- ✅ Async components for server-side data fetching

---

### 2. Better Auth Integration

**Configuration:**
```typescript
// lib/auth.ts
import { betterAuth } from "better-auth"
import { prismaAdapter } from "better-auth/adapters/prisma"

export const auth = betterAuth({
  database: prismaAdapter(prisma),
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false
  },
  JWT: {
    enabled: true,
    expiresIn: "7d"
  }
})
```

**Usage in Components:**
```tsx
import { auth } from "@/lib/auth"

export default async function LoginPage() {
  const session = await auth()

  if (session) {
    redirect('/dashboard')
  }

  return <SignupForm />
}
```

**Client Session Access:**
```tsx
'use client'

import { useSession } from "better-auth/react"

export function UserMenu() {
  const { data: session, status } = useSession()

  if (status === "loading") return <Skeleton />

  return (
    <div>
      <p>Welcome, {session?.user?.name}</p>
      <button onClick={() => auth.signOut()}>Sign out</button>
    </div>
  )
}
```

---

### 3. API Client Integration

**Centralized API Client:**
```typescript
// lib/api.ts
class ApiClient {
  private token: string | null = null

  setToken(token: string) {
    this.token = token
    localStorage.setItem('jwt_token', token)
  }

  clearToken() {
    this.token = null
    localStorage.removeItem('jwt_token')
  }

  private async request<T>(
    endpoint: string,
    options?: RequestInit
  ): Promise<T> {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...(this.token && { 'Authorization': `Bearer ${this.token}` })
    }

    const response = await fetch(`${API_BASE}${endpoint}`, {
      ...options,
      headers
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.error?.message || 'Request failed')
    }

    return response.json()
  }

  // Auth methods
  async signup(data: SignupData) {
    const response = await this.request<{success: boolean; data: {user: User; token: string}}>(
      '/api/v1/auth/signup',
      {
        method: 'POST',
        body: JSON.stringify(data)
      }
    )

    if (response.success) {
      this.setToken(response.data.token)
    }

    return response
  }

  async login(data: LoginData) {
    const response = await this.request<{success: boolean; data: {user: User; token: string}}>(
      '/api/v1/auth/login',
      {
        method: 'POST',
        body: JSON.stringify(data)
      }
    )

    if (response.success) {
      this.setToken(response.data.token)
    }

    return response
  }

  // Task methods
  async getTasks(params?: TaskParams) {
    const qs = new URLSearchParams(params).toString()
    return this.request<{success: boolean; data: {tasks: Task[]; pagination: PaginationInfo}}>(
      `/api/v1/tasks${qs ? `?${qs}` : ''}`
    )
  }

  async createTask(data: CreateTaskData) {
    return this.request<{success: boolean; data: Task}>(
      '/api/v1/tasks',
      {
        method: 'POST',
        body: JSON.stringify(data)
      }
    )
  }

  async updateTask(id: number, data: UpdateTaskData) {
    return this.request<{success: boolean; data: Task}>(
      `/api/v1/tasks/${id}`,
      {
        method: 'PUT',
        body: JSON.stringify(data)
      }
    )
  }

  async deleteTask(id: number) {
    return this.request<{success: boolean; data: {message: string}}>(
      `/api/v1/tasks/${id}`,
      { method: 'DELETE' }
    )
  }

  async toggleComplete(id: number) {
    return this.request<{success: boolean; data: Task}>(
      `/api/v1/tasks/${id}/complete`,
      { method: 'PATCH' }
    )
  }
}

export const api = new ApiClient()
```

**Usage:**
```tsx
import { api } from '@/lib/api'

// In server component
const tasks = await api.getTasks({ status: 'pending' })
```

---

### 4. Reusable UI Components

**Button Component:**
```tsx
// components/ui/button.tsx
import { ButtonHTMLAttributes } from 'react'

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost'
  size?: 'sm' | 'md' | 'lg'
  loading?: boolean
}

export function Button({
  variant = 'primary',
  size = 'md',
  loading = false,
  className = '',
  disabled,
  children,
  ...props
}: ButtonProps) {
  const baseClasses = 'rounded-lg font-medium transition-colors disabled:opacity-50'

  const variantClasses = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700',
    secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300',
    danger: 'bg-red-600 text-white hover:bg-red-700',
    ghost: 'bg-transparent text-gray-700 hover:bg-gray-100'
  }

  const sizeClasses = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg'
  }

  return (
    <button
      className={`${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]} ${className}`}
      disabled={disabled || loading}
      {...props}
    >
      {loading ? 'Loading...' : children}
    </button>
  )
}
```

**Input Component:**
```tsx
// components/ui/input.tsx
import { InputHTMLAttributes, forwardRef } from 'react'

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  error?: string
  label?: string
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ error, label, className = '', id, ...props }, ref
) => {
    const inputClasses = error
      ? 'border-red-500 focus:border-red-500'
      : 'border-gray-300 focus:border-blue-500'

    return (
      <div className="w-full">
        {label && (
          <label htmlFor={id} className="block text-sm font-medium text-gray-700 mb-1">
            {label}
          </label>
        )}
        <input
          id={id}
          className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${inputClasses} ${className}`}
          ref={ref}
          {...props}
        />
        {error && (
          <p className="text-sm text-red-500 mt-1">{error}</p>
        )}
      </div>
    )
  }
)
```

**Card Component:**
```tsx
// components/ui/card.tsx
import { HTMLAttributes } from 'react'

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'elevated' | 'bordered'
  padding?: 'none' | 'sm' | 'md' | 'lg'
}

export function Card({
  variant = 'default',
  padding = 'md',
  className = '',
  children,
  ...props
}: CardProps) {
  const baseClasses = 'rounded-lg'

  const variantClasses = {
    default: 'bg-white',
    elevated: 'bg-white shadow-md',
    bordered: 'bg-white border border-gray-200'
  }

  const paddingClasses = {
    none: '',
    sm: 'p-4',
    md: 'p-6',
    lg: 'p-8'
  }

  return (
    <div
      className={`${baseClasses} ${variantClasses[variant]} ${paddingClasses[padding]} ${className}`}
      {...props}
    >
      {children}
    </div>
  )
}
```

---

### 5. Form Components

**Login Form:**
```tsx
// components/forms/login-form.tsx
'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { api } from '@/lib/api'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'

export function LoginForm() {
  const router = useRouter()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const response = await api.login({ email, password })
      router.push('/dashboard')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-lg">
          {error}
        </div>
      )}

      <Input
        id="email"
        type="email"
        label="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
        placeholder="you@example.com"
      />

      <Input
        id="password"
        type="password"
        label="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
        minLength={8}
        placeholder="•••••••••"
      />

      <Button type="submit" loading={loading} className="w-full">
        {loading ? 'Logging in...' : 'Log in'}
      </Button>
    </form>
  )
}
```

---

### 6. Protected Routes

**Middleware Pattern:**
```typescript
// middleware.ts
import { auth } from "@/lib/auth"
import { NextResponse } from "next/server"

export default auth((req) => {
  const isAuthenticated = !!req.auth
  const isOnDashboard = req.nextUrl.pathname.startsWith('/dashboard')

  if (isOnDashboard && !isAuthenticated) {
    return NextResponse.redirect(new URL('/login', req.url))
  }

  if ((req.nextUrl.pathname === '/login' || req.nextUrl.pathname === '/signup') && isAuthenticated) {
    return NextResponse.redirect(new URL('/dashboard', req.url))
  }

  return NextResponse.next()
})

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)']
}
```

---

### 7. Responsive Design with Tailwind CSS

**Mobile-First Approach:**
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {/* 1 column on mobile, 2 on tablet, 3 on desktop */}
</div>

<button className="px-4 py-2 md:px-6 md:py-3 text-sm md:text-base">
  {/* Smaller padding on mobile */}
  Submit
</button>
```

**Common Tailwind Patterns:**
- Layout: `container mx-auto px-4`
- Flexbox: `flex justify-between items-center`
- Grid: `grid grid-cols-1 md:grid-cols-2`
- Spacing: `gap-4`, `space-y-4`
- Text: `text-sm`, `text-lg`, `font-bold`
- Colors: `bg-blue-600`, `text-gray-900`
- Responsive: `hidden md:block`, `block md:hidden`

---

### 8. TypeScript Type Definitions

**Global Types:**
```typescript
// types/index.ts
export interface User {
  id: string
  email: string
  name: string
  emailVerifiedAt: Date | null
  image: string | null
  createdAt: Date
}

export interface Task {
  id: number
  user_id: string
  title: string
  description: string | null
  completed: boolean
  created_at: Date
  updated_at: Date
}

export interface PaginationInfo {
  page: number
  limit: number
  total: number
  totalPages: number
}

export interface ApiResponse<T> {
  success: boolean
  data: T
}

export interface ApiError {
  success: false
  error: {
    code: string
    message: string
  }
}
```

---

### 9. Error Handling

**Error Boundary:**
```tsx
// components/error-boundary.tsx
'use client'

import { useEffect } from 'react'

export function ErrorBoundary({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  useEffect(() => {
    console.error(error)
  }, [error])

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
  )
}
```

**API Error Handling:**
```tsx
try {
  const data = await api.getTasks()
  setTasks(data.tasks)
} catch (error) {
  setError(error instanceof Error ? error.message : 'Failed to load tasks')
} finally {
  setLoading(false)
}
```

---

### 10. Loading States

**Loading Skeleton:**
```tsx
// components/ui/loading-skeleton.tsx
export function TaskSkeleton() {
  return (
    <div className="space-y-4">
      {[1, 2, 3].map((i) => (
        <div key={i} className="animate-pulse bg-gray-200 h-20 rounded-lg" />
      ))}
    </div>
  )
}

// Usage
function TaskList({ loading, tasks }: { loading: boolean; tasks: Task[] }) {
  if (loading) {
    return <TaskSkeleton />
  }

  return <div>{tasks.map(task => <TaskCard key={task.id} task={task} />)}</div>
}
```

---

## Quality Checklist

Before completing implementation:

- [ ] All pages use App Router structure
- [ ] Server components used by default
- [ ] Client components marked with 'use client'
- [ ] TypeScript types defined for all data
- [ ] API client centralized in lib/api.ts
- [ ] Better Auth configured correctly
- [ ] Protected routes use middleware
- [ ] Components are reusable
- [ ] Responsive design (mobile, tablet, desktop)
- [ ] Error boundaries implemented
- [ ] Loading states handled
- [ ] Forms have validation
- [ ] Tailwind CSS classes used consistently

---

## Common Patterns

### Pattern 1: Server Component with Data Fetching
```tsx
// app/dashboard/page.tsx
async function DashboardPage() {
  const response = await fetch(`${API_BASE}/api/v1/tasks`, {
    headers: { Authorization: `Bearer ${await getAuthToken()}` }
  })

  const { data } = await response.json()

  return <TaskList tasks={data.tasks} />
}
```

### Pattern 2: Client Component with Interactivity
```tsx
'use client'

export function TaskFormModal({ onSubmit, onCancel }) {
  const [title, setTitle] = useState('')
  const [isOpen, setIsOpen] = useState(false)

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    await onSubmit({ title })
    setIsOpen(false)
  }

  return (
    <>
      <button onClick={() => setIsOpen(true)}>New Task</button>
      {isOpen && (
        <Modal onClose={() => setIsOpen(false)}>
          <form onSubmit={handleSubmit}>
            <input value={title} onChange={(e) => setTitle(e.target.value)} />
            <button type="submit">Create</button>
            <button type="button" onClick={onCancel}>Cancel</button>
          </form>
        </Modal>
      )}
    </>
  )
}
```

### Pattern 3: Protected Route
```tsx
// app/dashboard/page.tsx
import { auth } from "@/lib/auth"

export default async function DashboardPage() {
  const session = await auth()

  if (!session) {
    redirect('/login')  // Unimplemented users get redirected
  }

  return <DashboardContent user={session.user} />
}
```

---

## Dependencies

### Required Packages:
```json
{
  "dependencies": {
    "next": "16.0.0",
    "react": "^19.0.0",
    "typescript": "^5",
    "better-auth": "^1.0.0",
    "tailwindcss": "^3.4.0",
    "@types/node": "^20",
    "clsx": "^2.1.0"
  }
}
```

### Install:
```bash
npx create-next-app@latest frontend
npm install better-auth
npm install tailwindcss clsx
```

---

## Related Skills

- `spec-writing` - Create specifications before implementing
- `system-architecture` - Design architecture before coding
- `fastapi-backend` - Backend API integration
- `qa-testing-validator` - Test implementation after completion

---

## Usage Instructions

When invoked, this skill will:

1. **Read Specification:** Review approved specs and architecture
2. **Setup Project:** Initialize Next.js with App Router
3. **Configure Auth:** Set up Better Auth with JWT
4. **Create API Client:** Build centralized API communication
5. **Build Components:** Create reusable UI components
6. **Implement Pages:** Build page routes with proper routing
7. **Add Forms:** Create interactive forms with validation
8. **Style UI:** Apply Tailwind CSS for responsive design
9. **Handle Errors:** Implement error boundaries and loading states
10. **Test:** Validate all functionality works

---

## File Locations

Implementation creates:
- Frontend code: `frontend/` directory
- Components: `frontend/components/` directory
- Pages: `frontend/app/` directory
- Libraries: `frontend/lib/` directory
- Styles: `frontend/styles/` directory
- Config: `frontend/package.json`, `frontend/next.config.js`

---

## Version History

- **v1.0** (2026-01-17): Initial skill definition

---

**Skill Status:** ✅ Active
**Phase:** Phase II - Full-Stack Web Application
