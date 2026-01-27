'use client';

/**
 * Signup Page with Neon Theme
 * Black background with neon cyan, pink, purple, green, yellow
 */

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { signupSchema, type SignupFormData } from '@/lib/validation';
import { useAuth } from '@/lib/auth';

export default function SignupPage() {
  const router = useRouter();
  const { signup } = useAuth();
  const [error, setError] = useState<string | null>(null);
  const [passwordStrength, setPasswordStrength] = useState<{
    score: number;
    label: string;
    color: string;
  }>({ score: 0, label: 'Weak', color: 'bg-red-500' });

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors, isSubmitting },
  } = useForm<SignupFormData>({
    resolver: zodResolver(signupSchema),
    mode: 'onBlur',
    defaultValues: {
      email: '',
      password: '',
      confirmPassword: '',
      name: undefined,
    },
  });

  const password = watch('password');

  const calculatePasswordStrength = (password: string) => {
    if (!password) {
      return { score: 0, label: 'Weak', color: 'bg-red-500' };
    }

    let score = 0;
    if (password.length >= 8) score++;
    if (password.length >= 12) score++;
    if (/[a-z]/.test(password)) score++;
    if (/[A-Z]/.test(password)) score++;
    if (/\d/.test(password)) score++;
    if (/[^a-zA-Z0-9]/.test(password)) score++;

    if (score <= 2) return { score, label: 'Weak', color: 'bg-red-500' };
    if (score <= 4) return { score, label: 'Medium', color: 'bg-yellow-500' };
    return { score, label: 'Strong', color: 'bg-green-500' };
  };

  useEffect(() => {
    if (password) {
      setPasswordStrength(calculatePasswordStrength(password));
    }
  }, [password]);

  const onSubmit = async (data: SignupFormData) => {
    try {
      setError(null);
      await signup({
        email: data.email,
        password: data.password,
        name: data.name,
      });

      router.push('/login');
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Signup failed';
      setError(message);
    }
  };

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h2 className="text-2xl font-bold text-white mb-2">
          Get Started
        </h2>
        <p className="text-sm text-white/60">
          Already have an account?{' '}
          <a
            href="/login"
            className="font-semibold hover:opacity-80"
            className="font-semibold hover:opacity-80 neon-text"
          >
            Log in →
          </a>
        </p>
      </div>

      {error && (
        <div className="bg-red-500/10 border border-red-500/30 text-red-300 px-4 py-3 rounded-xl">
          <div className="flex items-center">
            <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
            <span className="text-sm font-medium">{error}</span>
          </div>
        </div>
      )}

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div>
          <label htmlFor="name" className="block text-sm font-medium text-white/80 mb-1.5">
            Name <span className="text-white/50">(Optional)</span>
          </label>
          <input
            {...register('name')}
            type="text"
            id="name"
            className="w-full px-4 py-2.5 bg-white/5 border border-white/10 text-white placeholder-white/40 rounded-xl focus:border-white/20 focus:bg-white/10 focus:outline-none focus:ring-1 transition-all"
            placeholder="John Doe"
          />
          {errors.name && (
            <p className="mt-1 text-sm text-red-400">{errors.name.message}</p>
          )}
        </div>

        <div>
          <label htmlFor="email" className="block text-sm font-medium text-white/80 mb-1.5">
            Email Address
          </label>
          <input
            {...register('email')}
            type="email"
            id="email"
            className="w-full px-4 py-2.5 bg-white/5 border border-white/10 text-white placeholder-white/40 rounded-xl focus:border-white/20 focus:bg-white/10 focus:outline-none focus:ring-1 transition-all"
            placeholder="you@example.com"
          />
          {errors.email && (
            <p className="mt-1 text-sm text-red-400">{errors.email.message}</p>
          )}
        </div>

        <div>
          <label htmlFor="password" className="block text-sm font-medium text-white/80 mb-1.5">
            Password
          </label>
          <input
            {...register('password')}
            type="password"
            id="password"
            className="w-full px-4 py-2.5 bg-white/5 border border-white/10 text-white placeholder-white/40 rounded-xl focus:border-white/20 focus:bg-white/10 focus:outline-none focus:ring-1 transition-all"
            placeholder="••••••••"
          />
          {errors.password && (
            <p className="mt-1 text-sm text-red-400">{errors.password.message}</p>
          )}

          {password && (
            <div className="mt-3">
              <div className="flex items-center justify-between mb-1.5">
                <span className="text-xs text-white/50">Password strength:</span>
                <span className={`text-xs font-medium ${
                  passwordStrength.score <= 2 ? 'text-red-400' :
                  passwordStrength.score <= 4 ? 'text-yellow-400' :
                  'text-green-400'
                }`}>
                  {passwordStrength.label}
                </span>
              </div>
              <div className="w-full bg-white/10 rounded-full h-2">
                <div
                  className={`${passwordStrength.color} h-2 rounded-full transition-all duration-500`}
                  style={{ width: `${(passwordStrength.score / 6) * 100}%` }}
                />
              </div>
            </div>
          )}
        </div>

        <div>
          <label htmlFor="confirmPassword" className="block text-sm font-medium text-white/80 mb-1.5">
            Confirm Password
          </label>
          <input
            {...register('confirmPassword')}
            type="password"
            id="confirmPassword"
            className="w-full px-4 py-2.5 bg-white/5 border border-white/10 text-white placeholder-white/40 rounded-xl focus:border-white/20 focus:bg-white/10 focus:outline-none focus:ring-1 transition-all"
            placeholder="••••••••"
          />
          {errors.confirmPassword && (
            <p className="mt-1 text-sm text-red-400">{errors.confirmPassword.message}</p>
          )}
        </div>

        <button
          type="submit"
          disabled={isSubmitting}
          className="w-full py-3 px-4 text-black font-semibold rounded-xl transition-all duration-200 hover:opacity-90 hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
          style={{ background: '#00FFFF' }}
        >
          {isSubmitting ? (
            <span className="flex items-center justify-center">
              <svg className="animate-spin -ml-1 mr-2 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              Creating account...
            </span>
          ) : (
            'Create Account'
          )}
        </button>
      </form>

      <div className="text-xs text-white/50 bg-white/5 px-4 py-3 rounded-xl border border-white/10">
        <p className="font-medium mb-2">Password requirements:</p>
        <ul className="space-y-1">
          <li>• At least 8 characters</li>
          <li>• One uppercase letter</li>
          <li>• One lowercase letter</li>
          <li>• One digit</li>
          <li>• One special character</li>
        </ul>
      </div>
    </div>
  );
}
