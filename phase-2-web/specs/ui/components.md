# UI Components Specification

## Component Overview

This document defines all UI components for the Phase II Todo App frontend.

---

## Design System

### Color Palette

```css
/* Primary Colors */
--primary: #3b82f6;        /* Blue-500 */
--primary-hover: #2563eb;  /* Blue-600 */
--primary-light: #dbeafe;  /* Blue-100 */

/* Neutral Colors */
--background: #ffffff;
--surface: #f9fafb;        /* Gray-50 */
--border: #e5e7eb;         /* Gray-200 */
--text: #111827;           /* Gray-900 */
--text-muted: #6b7280;     /* Gray-500 */

/* Status Colors */
--success: #10b981;        /* Green-500 */
--danger: #ef4444;         /* Red-500 */
--warning: #f59e0b;        /* Amber-500 */
```

### Typography

```css
/* Font Family */
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;

/* Font Sizes */
--text-xs: 0.75rem;    /* 12px */
--text-sm: 0.875rem;   /* 14px */
--text-base: 1rem;     /* 16px */
--text-lg: 1.125rem;   /* 18px */
--text-xl: 1.25rem;    /* 20px */
--text-2xl: 1.5rem;    /* 24px */
```

### Spacing

```css
--spacing-xs: 0.25rem;  /* 4px */
--spacing-sm: 0.5rem;   /* 8px */
--spacing-md: 1rem;     /* 16px */
--spacing-lg: 1.5rem;   /* 24px */
--spacing-xl: 2rem;     /* 32px */
```

---

## Component Library

### 1. Button Component

**Purpose:** Reusable button for actions

**Variants:**
- `primary` - Main action buttons
- `secondary` - Alternative actions
- `danger` - Destructive actions
- `ghost` - Minimal styling

**Sizes:**
- `sm` - Small (32px height)
- `md` - Medium (40px height)
- `lg` - Large (48px height)

**States:**
- Default
- Hover
- Active
- Disabled
- Loading

**Props:**
```typescript
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  loading?: boolean;
  onClick?: () => void;
  children: React.ReactNode;
}
```

**Implementation:**
```tsx
// components/ui/button.tsx
export function Button({ variant = 'primary', size = 'md', ... }: ButtonProps) {
  const baseClasses = "rounded-lg font-medium transition-colors";
  const variantClasses = {
    primary: "bg-blue-500 text-white hover:bg-blue-600",
    secondary: "bg-gray-200 text-gray-900 hover:bg-gray-300",
    danger: "bg-red-500 text-white hover:bg-red-600",
    ghost: "bg-transparent text-gray-700 hover:bg-gray-100"
  };
  // ... implementation
}
```

---

### 2. Input Component

**Purpose:** Text input fields

**Variants:**
- Default
- With error
- Disabled

**Props:**
```typescript
interface InputProps {
  type?: 'text' | 'email' | 'password';
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  error?: string;
  disabled?: boolean;
  required?: boolean;
}
```

**Features:**
- Auto-focus support
- Character counter
- Error message display
- Label association

---

### 3. Card Component

**Purpose:** Container for related content

**Variants:**
- Default
- Elevated
- Bordered

**Props:**
```typescript
interface CardProps {
  children: React.ReactNode;
  variant?: 'default' | 'elevated' | 'bordered';
  padding?: 'none' | 'sm' | 'md' | 'lg';
}
```

---

### 4. TaskList Component

**Location:** `components/tasks/task-list.tsx`

**Purpose:** Display list of user's tasks

**Props:**
```typescript
interface TaskListProps {
  tasks: Task[];
  loading?: boolean;
  onEdit: (task: Task) => void;
  onDelete: (taskId: number) => void;
  onToggleComplete: (taskId: number) => void;
}
```

**Features:**
- Display tasks in list format
- Show task title and description preview
- Visual indication of completion (checkbox, strikethrough)
- Quick action buttons (Edit, Delete, Complete)
- Empty state when no tasks
- Loading skeleton during data fetch
- Error state with retry button
- Pagination controls

**States:**

**Loading State:**
```tsx
{loading && (
  <div className="space-y-4">
    {[1, 2, 3].map(i => (
      <div key={i} className="animate-pulse bg-gray-200 h-20 rounded-lg" />
    ))}
  </div>
)}
```

**Empty State:**
```tsx
{!loading && tasks.length === 0 && (
  <div className="text-center py-12">
    <div className="text-6xl mb-4">📝</div>
    <h3 className="text-lg font-semibold mb-2">No tasks yet</h3>
    <p className="text-gray-500">Create your first task to get started!</p>
  </div>
)}
```

**Error State:**
```tsx
{error && (
  <div className="bg-red-50 border border-red-200 rounded-lg p-4">
    <p className="text-red-600 mb-2">Failed to load tasks</p>
    <button onClick={retry} className="text-red-600 underline">Try again</button>
  </div>
)}
```

---

### 5. TaskCard Component

**Location:** `components/tasks/task-card.tsx`

**Purpose:** Display single task

**Props:**
```typescript
interface TaskCardProps {
  task: Task;
  onEdit: (task: Task) => void;
  onDelete: (taskId: number) => void;
  onToggleComplete: (taskId: number) => void;
}
```

**Visual Design:**
```tsx
<div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 hover:shadow-md transition-shadow">
  <div className="flex items-start gap-3">
    {/* Checkbox */}
    <input
      type="checkbox"
      checked={task.completed}
      onChange={() => onToggleComplete(task.id)}
      className="mt-1 w-5 h-5 rounded"
    />

    {/* Content */}
    <div className="flex-1 min-w-0">
      <h3 className={`font-semibold ${task.completed ? 'line-through text-gray-400' : ''}`}>
        {task.title}
      </h3>
      {task.description && (
        <p className="text-sm text-gray-500 mt-1 line-clamp-2">
          {task.description}
        </p>
      )}
      <div className="text-xs text-gray-400 mt-2">
        Created {formatDate(task.created_at)}
      </div>
    </div>

    {/* Actions */}
    <div className="flex gap-2">
      <button onClick={() => onEdit(task)} className="p-2 hover:bg-gray-100 rounded">
        <EditIcon />
      </button>
      <button onClick={() => onDelete(task.id)} className="p-2 hover:bg-red-50 rounded text-red-500">
        <DeleteIcon />
      </button>
    </div>
  </div>
</div>
```

---

### 6. TaskForm Component

**Location:** `components/tasks/task-form.tsx`

**Purpose:** Create or edit task form

**Props:**
```typescript
interface TaskFormProps {
  task?: Task;  // If provided, editing existing task
  onSubmit: (data: TaskCreateData) => Promise<void>;
  onCancel?: () => void;
}
```

**Features:**
- Title input (required)
- Description textarea (optional)
- Character counters for both fields
- Real-time validation
- Submit and cancel buttons
- Loading state during submission
- Success/error feedback

**Validation:**
```tsx
const [title, setTitle] = useState(task?.title || '');
const [description, setDescription] = useState(task?.description || '');
const [errors, setErrors] = useState<{title?: string}>({});

const validate = () => {
  const newErrors: {title?: string} = {};
  if (!title.trim()) {
    newErrors.title = 'Title is required';
  } else if (title.length > 200) {
    newErrors.title = 'Title must be 200 characters or less';
  }
  setErrors(newErrors);
  return Object.keys(newErrors).length === 0;
};
```

**UI Layout:**
```tsx
<form onSubmit={handleSubmit} className="space-y-4">
  {/* Title Field */}
  <div>
    <label htmlFor="title" className="block text-sm font-medium mb-1">
      Title <span className="text-red-500">*</span>
    </label>
    <Input
      id="title"
      value={title}
      onChange={setTitle}
      placeholder="Enter task title"
      error={errors.title}
      maxLength={200}
    />
    <div className="text-xs text-gray-400 mt-1">
      {title.length}/200 characters
    </div>
  </div>

  {/* Description Field */}
  <div>
    <label htmlFor="description" className="block text-sm font-medium mb-1">
      Description <span className="text-gray-400">(optional)</span>
    </label>
    <textarea
      id="description"
      value={description}
      onChange={(e) => setDescription(e.target.value)}
      placeholder="Add a description..."
      rows={4}
      maxLength={1000}
      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
    />
    <div className="text-xs text-gray-400 mt-1">
      {description.length}/1000 characters
    </div>
  </div>

  {/* Actions */}
  <div className="flex gap-3">
    <Button type="submit" loading={loading}>
      {task ? 'Update Task' : 'Create Task'}
    </Button>
    {onCancel && (
      <Button type="button" variant="ghost" onClick={onCancel}>
        Cancel
      </Button>
    )}
  </div>
</form>
```

---

### 7. TaskDetail Component

**Location:** `components/tasks/task-detail.tsx`

**Purpose:** View full task details

**Props:**
```typescript
interface TaskDetailProps {
  task: Task;
  onEdit: (task: Task) => void;
  onDelete: (taskId: number) => void;
}
```

**Features:**
- Display full task information
- Edit button
- Delete button with confirmation
- Back button to return to list
- Timestamp display (created, updated)

---

### 8. API Client

**Location:** `lib/api.ts`

**Purpose:** Centralized API communication

```typescript
class ApiClient {
  private token: string | null = null;

  setToken(token: string) {
    this.token = token;
    localStorage.setItem('jwt_token', token);
  }

  clearToken() {
    this.token = null;
    localStorage.removeItem('jwt_token');
  }

  private async request<T>(
    endpoint: string,
    options?: RequestInit
  ): Promise<T> {
    const headers = {
      'Content-Type': 'application/json',
      ...(this.token && { 'Authorization': `Bearer ${this.token}` })
    };

    const response = await fetch(`${API_BASE}${endpoint}`, {
      ...options,
      headers
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error.message);
    }

    return response.json();
  }

  // Auth methods
  async signup(data: SignupData) {
    return this.request<{success: boolean; data: {user: User; token: string}}>(
      '/api/v1/auth/signup',
      { method: 'POST', body: JSON.stringify(data) }
    );
  }

  async login(data: LoginData) {
    const response = await this.request<{success: boolean; data: {user: User; token: string}}>(
      '/api/v1/auth/login',
      { method: 'POST', body: JSON.stringify(data) }
    );
    if (response.success) {
      this.setToken(response.data.token);
    }
    return response;
  }

  async logout() {
    await this.request('/api/v1/auth/logout', { method: 'POST' });
    this.clearToken();
  }

  // Task methods
  async getTasks(params?: TaskParams) {
    const qs = new URLSearchParams(params).toString();
    return this.request<{success: boolean; data: {tasks: Task[]; pagination: PaginationInfo}}>(
      `/api/v1/tasks${qs ? `?${qs}` : ''}`
    );
  }

  async createTask(data: CreateTaskData) {
    return this.request<{success: boolean; data: Task}>(
      '/api/v1/tasks',
      { method: 'POST', body: JSON.stringify(data) }
    );
  }

  async updateTask(id: number, data: UpdateTaskData) {
    return this.request<{success: boolean; data: Task}>(
      `/api/v1/tasks/${id}`,
      { method: 'PUT', body: JSON.stringify(data) }
    );
  }

  async deleteTask(id: number) {
    return this.request<{success: boolean; data: {message: string}}>(
      `/api/v1/tasks/${id}`,
      { method: 'DELETE' }
    );
  }

  async toggleComplete(id: number) {
    return this.request<{success: boolean; data: Task}>(
      `/api/v1/tasks/${id}/complete`,
      { method: 'PATCH' }
    );
  }
}

export const api = new ApiClient();
```

---

### 9. LoadingSpinner Component

**Purpose:** Indicate loading state

```tsx
// components/ui/loading-spinner.tsx
export function LoadingSpinner({ size = 'md' }: { size?: 'sm' | 'md' | 'lg' }) {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-12 h-12'
  };

  return (
    <div className={`border-4 border-blue-500 border-t-transparent rounded-full animate-spin ${sizeClasses[size]}`} />
  );
}
```

---

### 10. Modal Component

**Purpose:** Overlay for dialogs and forms

```tsx
// components/ui/modal.tsx
interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
}

export function Modal({ isOpen, onClose, title, children }: ModalProps) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* Backdrop */}
      <div className="absolute inset-0 bg-black/50" onClick={onClose} />

      {/* Modal Content */}
      <div className="relative bg-white rounded-lg shadow-xl max-w-md w-full mx-4 p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold">{title}</h2>
          <button onClick={onClose} className="p-2 hover:bg-gray-100 rounded">
            ✕
          </button>
        </div>
        {children}
      </div>
    </div>
  );
}
```

---

### 11. Toast Notification Component

**Purpose:** Display success/error messages

```tsx
// components/ui/toast.tsx
interface ToastProps {
  message: string;
  type: 'success' | 'error';
  onClose: () => void;
}

export function Toast({ message, type, onClose }: ToastProps) {
  const bgColor = type === 'success' ? 'bg-green-500' : 'bg-red-500';

  return (
    <div className={`fixed bottom-4 right-4 ${bgColor} text-white px-6 py-3 rounded-lg shadow-lg flex items-center gap-3`}>
      <span>{type === 'success' ? '✅' : '❌'}</span>
      <span>{message}</span>
      <button onClick={onClose} className="ml-2 hover:opacity-80">✕</button>
    </div>
  );
}
```

---

## Component Hierarchy

```
app/
├── layout.tsx                # Root layout
│   ├── Header
│   └── main content
│
├── (auth)/
│   ├── login/page.tsx
│   │   └── LoginForm
│   └── signup/page.tsx
│       └── SignupForm
│
└── dashboard/
    ├── page.tsx
    │   ├── TaskList
    │   │   └── TaskCard (multiple)
    │   └── TaskForm
    │
    └── tasks/[id]/
        └── page.tsx
            └── TaskDetail
```

---

## Icons

**Using:** Lucide React (recommended)

```bash
npm install lucide-react
```

**Usage:**
```tsx
import { Check, Edit, Trash, Plus } from 'lucide-react';

<Plus className="w-5 h-5" />
<Edit className="w-5 h-5" />
<Trash className="w-5 h-5" />
<Check className="w-5 h-5" />
```

---

## Responsive Design

### Breakpoints

```css
/* Mobile First */
--sm: 640px;    /* Small devices */
--md: 768px;    /* Medium devices (tablets) */
--lg: 1024px;   /* Large devices (desktops) */
--xl: 1280px;   /* Extra large devices */
```

**Example:**
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {/* Responsive grid */}
</div>
```

---

## Accessibility

**ARIA Labels:**
```tsx
<button aria-label="Delete task" onClick={onDelete}>
  <TrashIcon />
</button>
```

**Keyboard Navigation:**
```tsx
<div
  role="button"
  tabIndex={0}
  onKeyDown={(e) => e.key === 'Enter' && onClick()}
  onClick={onClick}
>
  Task content
</div>
```

**Screen Reader Support:**
```tsx
<div aria-live="polite" aria-atomic="true">
  {error && <div role="alert">{error}</div>}
</div>
```

---

## Related Specifications

- **Overview:** `@specs/overview.md`
- **Architecture:** `@specs/architecture.md`
- **Features:** `@specs/features/`
- **API:** `@specs/api/rest-endpoints.md`
- **Database:** `@specs/database/schema.md`
- **Pages:** `@specs/ui/pages.md`

---

**Document Status:** ✅ Ready for Review
**Last Updated:** January 17, 2026
**Phase:** Phase II - Full-Stack Web Application
