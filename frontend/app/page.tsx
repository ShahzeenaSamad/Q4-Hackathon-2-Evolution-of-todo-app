'use client';

/**
 * Landing Page with Custom Color Palette
 * #092635, #1B4242, #5C8374, #9EC8B9
 */

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function Home() {
  const router = useRouter();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  const features = [
    {
      icon: '🎯',
      title: 'Smart Task Management',
      description: 'Organize tasks with priority levels, due dates, and categories'
    },
    {
      icon: '⚡',
      title: 'Lightning Fast',
      description: 'Real-time updates with instant sync across all your devices'
    },
    {
      icon: '📊',
      title: 'Productivity Insights',
      description: 'Track your progress with beautiful analytics and statistics'
    },
    {
      icon: '🎨',
      title: 'Beautiful Design',
      description: 'Modern dark UI with smooth animations'
    }
  ];

  if (!mounted) return null;

  return (
    <div className="min-h-screen" style={{ background: 'linear-gradient(to bottom right, #092635, #1B4242)' }}>
      {/* Animated background blobs */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden">
        <div className="absolute top-20 left-10 w-96 h-96 rounded-full opacity-40 animate-blob blur-2xl" style={{ background: 'linear-gradient(to right, #5C8374, #9EC8B9)', animationDelay: '0s' }}></div>
        <div className="absolute top-40 right-10 w-[500px] h-[500px] rounded-full opacity-40 animate-blob blur-2xl" style={{ background: 'linear-gradient(to right, #1B4242, #5C8374)', animationDelay: '2s' }}></div>
        <div className="absolute bottom-20 left-1/3 w-[450px] h-[450px] rounded-full opacity-40 animate-blob blur-2xl" style={{ background: 'linear-gradient(to right, #9EC8B9, #1B4242)', animationDelay: '4s' }}></div>
      </div>

      {/* Navigation */}
      <div className="relative z-10 px-6 py-4 border-b border-white/10 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-3 group cursor-pointer" onClick={() => router.push('/')}>
            <div className="p-2.5 rounded-xl transition-all duration-300 hover:scale-110 hover:shadow-lg animate-bounce-slow" style={{ background: 'linear-gradient(to bottom right, #5C8374, #9EC8B9)' }}>
              <svg className="w-7 h-7 text-white animate-spin-slow" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
              </svg>
            </div>
            <span className="text-2xl font-bold text-white transition-all duration-300 hover:scale-105 animate-gradient-x" style={{ backgroundImage: 'linear-gradient(to right, #9EC8B9, #5C8374, #9EC8B9)', backgroundSize: '200% 100%', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>TaskFlow</span>
          </div>
          <div className="flex items-center space-x-4">
            <button
              onClick={() => router.push('/login')}
              className="px-6 py-2.5 text-white/80 font-medium hover:text-white rounded-lg transition-all duration-200 hover:bg-white/10 hover:scale-105"
            >
              Log In
            </button>
            <button
              onClick={() => router.push('/signup')}
              className="px-6 py-2.5 text-white font-semibold rounded-lg transition-all duration-200 hover:shadow-xl hover:opacity-90 hover:scale-105"
              style={{ background: 'linear-gradient(to right, #5C8374, #9EC8B9)' }}
            >
              Get Started
            </button>
          </div>
        </div>
      </div>

      <main className="relative z-10 px-6 pt-20 pb-32">
        <div className="max-w-7xl mx-auto text-center">
          {/* Animated icons */}
          <div className="flex justify-center items-center space-x-8 mb-12">
            <span className="text-4xl animate-bounce" style={{ animationDelay: '0s' }}>👤</span>
            <span className="text-4xl animate-bounce" style={{ animationDelay: '0.2s' }}>📝</span>
            <span className="text-4xl animate-bounce" style={{ animationDelay: '0.4s' }}>✅</span>
            <span className="text-4xl animate-bounce" style={{ animationDelay: '0.6s' }}>📅</span>
            <span className="text-4xl animate-bounce" style={{ animationDelay: '0.8s' }}>🎯</span>
          </div>

          {/* Hero heading */}
          <h1 className="text-5xl md:text-7xl font-bold text-white mb-6 leading-tight">
            Organize. Prioritize.
            <br />
            <span className="bg-clip-text text-transparent animate-gradient-x" style={{ backgroundImage: 'linear-gradient(to right, #9EC8B9, #5C8374, #9EC8B9)', backgroundSize: '200% 100%' }}>
              Achieve.
            </span>
          </h1>

          {/* Subheading */}
          <p className="text-xl text-white/70 mb-12 max-w-2xl mx-auto">
            The todo app built for focus and productivity.
            <br />
            Manage tasks efficiently and get things done.
          </p>

          {/* CTA buttons */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-20">
            <button
              onClick={() => router.push('/signup')}
              className="group px-8 py-4 text-white font-semibold rounded-xl transition-all duration-300 hover:shadow-2xl hover:opacity-90 hover:scale-110 hover:-translate-y-1 w-full sm:w-auto"
              style={{ background: 'linear-gradient(to right, #5C8374, #9EC8B9)' }}
            >
              Start Organizing
              <svg className="inline-block w-5 h-5 ml-2 group-hover:translate-x-2 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </button>
            <button
              onClick={() => router.push('/login')}
              className="px-8 py-4 text-white font-medium rounded-xl border border-white/20 hover:border-white/30 hover:bg-white/10 transition-all duration-300 hover:scale-110 hover:-translate-y-1 w-full sm:w-auto hover:shadow-xl"
            >
              Sign In →
            </button>
          </div>

          {/* Feature cards with hover animations */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-6xl mx-auto">
            {features.map((feature, index) => (
              <div
                key={index}
                className="group bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-6 hover:border-white/20 hover:bg-white/10 transition-all duration-300 hover:scale-105 hover:-translate-y-2 hover:shadow-2xl cursor-pointer"
              >
                <div className="text-4xl mb-3 transition-transform duration-300 group-hover:scale-125 group-hover:rotate-12">{feature.icon}</div>
                <h3 className="text-lg font-semibold text-white mb-2 transition-colors duration-300 group-hover:text-transparent group-hover:bg-clip-text group-hover:bg-gradient-to-r group-hover:from-[#9EC8B9] group-hover:to-[#5C8374]">{feature.title}</h3>
                <p className="text-sm text-white/60">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="relative z-10 px-6 py-8 border-t border-white/10">
        <div className="max-w-7xl mx-auto text-center text-white/50">
          <p>&copy; 2026 TaskFlow. Built for productivity.</p>
        </div>
      </footer>
    </div>
  );
}
