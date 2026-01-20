'use client';

/**
 * Dashboard with Custom Color Palette
 * #092635, #1B4242, #5C8374, #9EC8B9
 */

import { useState, useEffect } from 'react';
import { useAuth } from '@/lib/auth';
import AuthGuard from '@/components/auth-guard';
import { useRouter } from 'next/navigation';
import { getTasks } from '@/lib/tasks';
import { Task } from '@/lib/types';
import TaskForm from '@/components/task-form';
import TaskList from '@/components/task-list';

export default function DashboardPage() {
  const { user, logout } = useAuth();
  const router = useRouter();

  // Task state
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [editTask, setEditTask] = useState<Task | null>(null);
  const [mounted, setMounted] = useState(false);

  // Search and filter state
  const [searchQuery, setSearchQuery] = useState('');
  const [filterStatus, setFilterStatus] = useState<'all' | 'pending' | 'completed'>('all');
  const [filterPriority, setFilterPriority] = useState<'all' | 'high' | 'medium' | 'low'>('all');
  const [filterCategory, setFilterCategory] = useState<string>('');

  const handleLogout = async () => {
    await logout();
    router.push('/login');
  };

  // Fetch tasks on mount
  const fetchTasks = async () => {
    setLoading(true);
    setError(null);
    try {
      const fetchedTasks = await getTasks();
      setTasks(fetchedTasks);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to fetch tasks';
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    setMounted(true);
    fetchTasks();
  }, []);

  // Get unique categories
  const categories = Array.from(new Set(tasks.map(t => t.category).filter(Boolean)));

  // Filter and search tasks
  const filteredTasks = tasks.filter(task => {
    // Search filter
    const matchesSearch = searchQuery === '' ||
      task.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (task.description && task.description.toLowerCase().includes(searchQuery.toLowerCase()));

    // Status filter
    const matchesStatus = filterStatus === 'all' ||
      (filterStatus === 'completed' && task.completed) ||
      (filterStatus === 'pending' && !task.completed);

    // Priority filter
    const matchesPriority = filterPriority === 'all' || task.priority === filterPriority;

    // Category filter
    const matchesCategory = filterCategory === '' || task.category === filterCategory;

    return matchesSearch && matchesStatus && matchesPriority && matchesCategory;
  });

  // Calculate stats
  const totalTasks = tasks.length;
  const completedTasks = tasks.filter(t => t.completed).length;
  const pendingTasks = totalTasks - completedTasks;
  const completionRate = totalTasks > 0 ? Math.round((completedTasks / totalTasks) * 100) : 0;

  if (!mounted) return null;

  return (
    <AuthGuard>
      <div className="min-h-screen" style={{ background: 'linear-gradient(to bottom right, #092635, #1B4242)' }}>
        {/* Header */}
        <header className="sticky top-0 z-50 backdrop-blur-xl border-b border-white/10">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
            <div className="flex justify-between items-center">
              <div className="flex items-center space-x-4">
                <div className="rounded-xl p-2.5 transition-all duration-300 hover:scale-110 hover:shadow-lg animate-bounce-slow" style={{ background: 'linear-gradient(to bottom right, #5C8374, #9EC8B9)' }}>
                  <svg className="w-7 h-7 text-white animate-spin-slow" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                  </svg>
                </div>
                <div>
                  <h1 className="text-2xl font-bold text-white transition-all duration-300 hover:scale-105 animate-gradient-x" style={{ backgroundImage: 'linear-gradient(to right, #9EC8B9, #5C8374, #9EC8B9)', backgroundSize: '200% 100%', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>TaskFlow</h1>
                  <p className="text-sm text-white/60">
                    Hey, {user?.name || user?.email?.split('@')[0]}!
                  </p>
                </div>
              </div>
              <button
                onClick={handleLogout}
                className="px-4 py-2 text-white/80 hover:text-white border border-white/20 hover:border-white/30 rounded-lg transition-all duration-200 hover:bg-white/10 flex items-center space-x-2"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
                <span>Logout</span>
              </button>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            {/* Total Tasks Card */}
            <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-6 hover:border-white/20 transition-all duration-200">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-white/60 mb-1">Total Tasks</p>
                  <p className="text-4xl font-bold text-white">{totalTasks}</p>
                </div>
                <div className="p-4 rounded-2xl" style={{ background: 'linear-gradient(to bottom right, rgba(165,56,96,0.3), rgba(158,200,185,0.3))' }}>
                  <svg className="w-10 h-10" style={{ color: '#9EC8B9' }} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                  </svg>
                </div>
              </div>
            </div>

            {/* Completed Tasks Card */}
            <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-6 hover:border-white/20 transition-all duration-200">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-white/60 mb-1">Completed</p>
                  <p className="text-4xl font-bold text-white">{completedTasks}</p>
                </div>
                <div className="p-4 rounded-2xl bg-green-500/20">
                  <svg className="w-10 h-10 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
              </div>
            </div>

            {/* Pending Tasks Card */}
            <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-6 hover:border-white/20 transition-all duration-200">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-white/60 mb-1">Pending</p>
                  <p className="text-4xl font-bold text-white">{pendingTasks}</p>
                </div>
                <div className="p-4 rounded-2xl bg-amber-500/20">
                  <svg className="w-10 h-10 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
              </div>
            </div>
          </div>

          {/* Progress Bar */}
          {totalTasks > 0 && (
            <div className="mb-8 bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-6">
              <div className="flex justify-between items-center mb-3">
                <span className="text-lg font-semibold text-white">Your Progress</span>
                <span className="text-2xl font-bold text-white">{completionRate}%</span>
              </div>
              <div className="w-full bg-white/10 rounded-full h-3 overflow-hidden">
                <div
                  className="h-3 rounded-full transition-all duration-700 ease-out"
                  style={{
                    width: `${completionRate}%`,
                    background: 'linear-gradient(to right, #5C8374, #9EC8B9)'
                  }}
                />
              </div>
              <p className="text-sm text-white/60 mt-2">
                {completedTasks} of {totalTasks} tasks completed! {completionRate === 100 ? '🎉 Great job!' : ''}
              </p>
            </div>
          )}

          {/* Two Column Layout */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Task Form - Left Column */}
            <div className="lg:col-span-1">
              <div className="lg:sticky lg:top-24">
                <TaskForm
                  onSuccess={fetchTasks}
                  editTask={editTask}
                  onCancelEdit={() => setEditTask(null)}
                />
              </div>
            </div>

            {/* Task List - Right Column */}
            <div className="lg:col-span-2">
              <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-6">
                <div className="flex justify-between items-center mb-6">
                  <div>
                    <h2 className="text-xl font-bold text-white">Your Tasks</h2>
                    <p className="text-sm text-white/60 mt-1">Manage and track your daily tasks</p>
                  </div>
                  {loading && (
                    <div className="flex items-center space-x-3">
                      <div className="w-6 h-6 border-3 border-white/20 rounded-full animate-spin" style={{ borderTopColor: '#9EC8B9' }}></div>
                      <span className="text-sm text-white/60">Loading...</span>
                    </div>
                  )}
                </div>

                {/* Search and Filters */}
                <div className="mb-6 space-y-4">
                  {/* Search Bar */}
                  <div className="relative">
                    <input
                      type="text"
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                      placeholder="🔍 Search tasks..."
                      className="w-full px-4 py-3 pl-12 bg-white/5 backdrop-blur-sm border-2 border-white/20 rounded-2xl text-white placeholder-white/40 focus:border-white/30 focus:outline-none transition-all"
                    />
                  </div>

                  {/* Filter Buttons */}
                  <div className="flex flex-wrap gap-3">
                    {/* Status Filter */}
                    <div className="flex rounded-2xl bg-white/5 backdrop-blur-sm border-2 border-white/20 p-1">
                      <button
                        onClick={() => setFilterStatus('all')}
                        className={`px-4 py-2 rounded-xl text-sm font-medium transition-all ${
                          filterStatus === 'all'
                            ? 'text-white shadow-lg'
                            : 'text-white/60 hover:text-white hover:bg-white/10'
                        }`}
                      >
                        All
                      </button>
                      <button
                        onClick={() => setFilterStatus('pending')}
                        className={`px-4 py-2 rounded-xl text-sm font-medium transition-all ${
                          filterStatus === 'pending'
                            ? 'text-white shadow-lg'
                            : 'text-white/60 hover:text-white hover:bg-white/10'
                        }`}
                      >
                        Pending
                      </button>
                      <button
                        onClick={() => setFilterStatus('completed')}
                        className={`px-4 py-2 rounded-xl text-sm font-medium transition-all ${
                          filterStatus === 'completed'
                            ? 'text-white shadow-lg'
                            : 'text-white/60 hover:text-white hover:bg-white/10'
                        }`}
                      >
                        Completed
                      </button>
                    </div>

                    {/* Priority Filter */}
                    <select
                      value={filterPriority}
                      onChange={(e) => setFilterPriority(e.target.value as 'all' | 'high' | 'medium' | 'low')}
                      className="px-4 py-3 bg-white/5 backdrop-blur-sm border-2 border-white/20 rounded-2xl text-white text-sm focus:border-white/30 focus:outline-none transition-all"
                    >
                      <option value="all" className="bg-gray-800">All Priorities</option>
                      <option value="high" className="bg-gray-800">🔴 High</option>
                      <option value="medium" className="bg-gray-800">🟡 Medium</option>
                      <option value="low" className="bg-gray-800">🟢 Low</option>
                    </select>

                    {/* Category Filter */}
                    {categories.length > 0 && (
                      <select
                        value={filterCategory}
                        onChange={(e) => setFilterCategory(e.target.value)}
                        className="px-4 py-3 bg-white/5 backdrop-blur-sm border-2 border-white/20 rounded-2xl text-white text-sm focus:border-white/30 focus:outline-none transition-all"
                      >
                        <option value="" className="bg-gray-800">All Categories</option>
                        {categories.map(cat => (
                          <option key={cat} value={cat} className="bg-gray-800">{cat}</option>
                        ))}
                      </select>
                    )}
                  </div>

                  {/* Results Count */}
                  <div className="text-sm text-white/60">
                    Showing {filteredTasks.length} of {tasks.length} tasks
                  </div>
                </div>

                {error && (
                  <div className="mb-6 bg-red-500/10 border border-red-500/30 text-red-300 px-4 py-3 rounded-xl flex items-center justify-between">
                    <div className="flex items-center">
                      <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                      </svg>
                      <span className="text-sm font-medium">{error}</span>
                    </div>
                    <button
                      onClick={fetchTasks}
                      className="px-3 py-1.5 bg-red-500/20 hover:bg-red-500/30 text-red-300 rounded-lg text-sm font-medium transition-all"
                    >
                      Retry
                    </button>
                  </div>
                )}

                {editTask && (
                  <div className="mb-6 px-4 py-3 rounded-xl flex items-center" style={{ background: 'rgba(158,200,185,0.15)', border: '1px solid rgba(158,200,185,0.3)', color: '#9EC8B9' }}>
                    <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                    </svg>
                    <span className="text-sm font-medium">Editing: <strong>{editTask.title}</strong></span>
                  </div>
                )}

                <TaskList
                  tasks={filteredTasks}
                  onTasksChange={fetchTasks}
                  onEditTask={setEditTask}
                />

                {!loading && filteredTasks.length === 0 && (
                  <div className="text-center py-16">
                    <div className="inline-flex items-center justify-center w-20 h-20 bg-white/10 rounded-full mb-4">
                      <svg className="w-10 h-10" style={{ color: '#9EC8B9' }} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                      </svg>
                    </div>
                    <h3 className="text-xl font-semibold text-white mb-2">
                      {searchQuery || filterStatus !== 'all' || filterPriority !== 'all' || filterCategory ? 'No tasks match your filters' : 'No tasks yet'}
                    </h3>
                    <p className="text-white/60">
                      {searchQuery || filterStatus !== 'all' || filterPriority !== 'all' || filterCategory ? 'Try adjusting your filters' : 'Create your first task to get started!'}
                    </p>
                  </div>
                )}
              </div>
            </div>
          </div>
        </main>
      </div>
    </AuthGuard>
  );
}
