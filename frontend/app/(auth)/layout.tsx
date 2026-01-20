/**
 * Authentication Layout with Custom Color Palette
 * #092635, #1B4242, #5C8374, #9EC8B9
 */

import { ReactNode } from 'react';

export default function AuthLayout({
  children,
}: {
  children: ReactNode;
}) {
  return (
    <div className="min-h-screen" style={{ background: 'linear-gradient(to bottom right, #092635, #1B4242)' }}>
      <div className="min-h-screen flex items-center justify-center p-4">
        <div className="w-full max-w-md">
          <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl shadow-2xl p-8">
            <div className="text-center mb-8">
              <div className="inline-flex items-center justify-center w-16 h-16 mb-4">
                <div className="rounded-2xl p-3 shadow-lg animate-bounce-slow transition-all duration-300 hover:scale-110 hover:shadow-xl" style={{ background: 'linear-gradient(to bottom right, #5C8374, #9EC8B9)' }}>
                  <svg className="w-10 h-10 text-white animate-spin-slow" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                  </svg>
                </div>
              </div>
              <h1 className="text-3xl font-bold text-white mb-2 animate-gradient-x" style={{ backgroundImage: 'linear-gradient(to right, #9EC8B9, #5C8374, #9EC8B9)', backgroundSize: '200% 100%', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>TaskFlow</h1>
              <p className="text-sm text-white/60">
                Your productivity journey starts here
              </p>
            </div>

            {children}
          </div>

          <div className="text-center mt-6 text-sm text-white/50">
            <p>&copy; 2026 TaskFlow. Built for productivity.</p>
          </div>
        </div>
      </div>
    </div>
  );
}
