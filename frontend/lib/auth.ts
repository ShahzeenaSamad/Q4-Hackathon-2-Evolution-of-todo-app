/**
 * Authentication utilities and hooks for Next.js frontend.
 *
 * Provides JWT-based authentication with:
 * - Access tokens in memory (expires in 15 minutes)
 * - Refresh tokens in localStorage (expires in 7 days)
 * - Automatic token refresh before expiration
 * - Session persistence across page refreshes
 */

import { useState, useEffect, useCallback } from 'react';
import { User, AuthTokens, AuthResponse, LoginRequest, SignupRequest } from './types';

// API base URL from environment
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Token storage keys
const REFRESH_TOKEN_KEY = 'refresh_token';
const USER_KEY = 'user';

// Token expiration times (must match backend)
const ACCESS_TOKEN_EXPIRE_MS = 15 * 60 * 1000; // 15 minutes
const REFRESH_THRESHOLD_MS = 2 * 60 * 1000; // Refresh 2 minutes before expiration

/**
 * In-memory token store (access tokens only for security)
 */
const inMemoryTokens: {
  accessToken: string | null;
  refreshToken: string | null;
  user: User | null;
} = {
  accessToken: null,
  refreshToken: null,
  user: null,
};

/**
 * Token refresh timer
 */
let refreshTimer: NodeJS.Timeout | null = null;

/**
 * Initialize auth state from localStorage on app load
 */
export function initializeAuth(): void {
  if (typeof window === 'undefined') return;

  const refreshToken = localStorage.getItem(REFRESH_TOKEN_KEY);
  const userStr = localStorage.getItem(USER_KEY);

  if (refreshToken) {
    inMemoryTokens.refreshToken = refreshToken;
  }

  if (userStr) {
    try {
      inMemoryTokens.user = JSON.parse(userStr);
    } catch (e) {
      console.error('Failed to parse user from localStorage:', e);
      localStorage.removeItem(USER_KEY);
    }
  }
}

/**
 * Store auth tokens after successful login/signup
 */
export function setAuthTokens(authResponse: AuthResponse): void {
  if (typeof window === 'undefined') return;

  // Check if response is successful
  if (!authResponse.success || !authResponse.data) {
    throw new Error(authResponse.error?.message || 'Authentication failed');
  }

  const { user, tokens } = authResponse.data;

  // Store access token in memory only (more secure)
  inMemoryTokens.accessToken = tokens.access_token;

  // Store refresh token in localStorage for persistence
  localStorage.setItem(REFRESH_TOKEN_KEY, tokens.refresh_token);

  // Store user info
  if (user) {
    inMemoryTokens.user = user;
    localStorage.setItem(USER_KEY, JSON.stringify(user));
  }

  // Schedule automatic token refresh
  scheduleTokenRefresh();
}

/**
 * Clear all auth tokens (logout)
 */
export function clearAuthTokens(): void {
  if (typeof window === 'undefined') return;

  // Clear in-memory tokens
  inMemoryTokens.accessToken = null;
  inMemoryTokens.refreshToken = null;
  inMemoryTokens.user = null;

  // Clear localStorage
  localStorage.removeItem(REFRESH_TOKEN_KEY);
  localStorage.removeItem(USER_KEY);

  // Cancel refresh timer
  if (refreshTimer) {
    clearTimeout(refreshTimer);
    refreshTimer = null;
  }
}

/**
 * Get current access token from memory
 */
export function getAccessToken(): string | null {
  return inMemoryTokens.accessToken;
}

/**
 * Get current refresh token from memory/localStorage
 */
export function getRefreshToken(): string | null {
  return inMemoryTokens.refreshToken;
}

/**
 * Get current user from memory
 */
export function getCurrentUser(): User | null {
  return inMemoryTokens.user;
}

/**
 * Check if user is authenticated
 */
export function isAuthenticated(): boolean {
  return !!inMemoryTokens.accessToken && !!inMemoryTokens.user;
}

/**
 * Schedule automatic token refresh before expiration
 */
function scheduleTokenRefresh(): void {
  // Cancel existing timer
  if (refreshTimer) {
    clearTimeout(refreshTimer);
  }

  // Schedule refresh 2 minutes before expiration
  refreshTimer = setTimeout(
    () => {
      refreshAccessToken().catch(() => {
        // If refresh fails, logout user
        clearAuthTokens();
        window.location.href = '/login';
      });
    },
    ACCESS_TOKEN_EXPIRE_MS - REFRESH_THRESHOLD_MS
  );
}

/**
 * Refresh access token using refresh token
 */
export async function refreshAccessToken(): Promise<AuthTokens> {
  const refreshToken = getRefreshToken();

  if (!refreshToken) {
    throw new Error('No refresh token available');
  }

  const response = await fetch(`${API_URL}/api/v1/auth/refresh`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ refresh_token: refreshToken }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to refresh token');
  }

  const authResponse: AuthResponse = await response.json();

  // Check if response is successful
  if (!authResponse.success || !authResponse.data) {
    throw new Error(authResponse.error?.message || 'Token refresh failed');
  }

  const { user, tokens } = authResponse.data;

  // Update tokens
  inMemoryTokens.accessToken = tokens.access_token;
  localStorage.setItem(REFRESH_TOKEN_KEY, tokens.refresh_token);

  // Update user info
  if (user) {
    inMemoryTokens.user = user;
    localStorage.setItem(USER_KEY, JSON.stringify(user));
  }

  // Reschedule next refresh
  scheduleTokenRefresh();

  return tokens;
}

/**
 * API request wrapper with automatic token injection and refresh
 */
export async function apiRequest(
  endpoint: string,
  options: RequestInit = {}
): Promise<Response> {
  let accessToken = getAccessToken();

  // Inject access token if available
  if (accessToken) {
    options.headers = {
      ...options.headers,
      Authorization: `Bearer ${accessToken}`,
    };
  }

  let response = await fetch(`${API_URL}${endpoint}`, options);

  // If 401, try to refresh token and retry
  if (response.status === 401 && getRefreshToken()) {
    try {
      await refreshAccessToken();
      accessToken = getAccessToken();

      // Retry original request with new token
      if (accessToken) {
        options.headers = {
          ...options.headers,
          Authorization: `Bearer ${accessToken}`,
        };
      }

      response = await fetch(`${API_URL}${endpoint}`, options);
    } catch {
      // Refresh failed, clear tokens and redirect to login
      clearAuthTokens();
      if (typeof window !== 'undefined') {
        window.location.href = '/login';
      }
      throw new Error('Session expired. Please login again.');
    }
  }

  return response;
}

/**
 * Login with email and password
 */
export async function login(credentials: LoginRequest): Promise<AuthResponse> {
  const response = await fetch(`${API_URL}/api/v1/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(credentials),
  });

  if (!response.ok) {
    const error = await response.json();
    const errorMessage = error.detail || error.error?.message || 'Login failed';
    throw new Error(errorMessage);
  }

  const data: AuthResponse = await response.json();
  setAuthTokens(data);
  return data;
}

/**
 * Sign up new user
 */
export async function signup(userData: SignupRequest): Promise<AuthResponse> {
  const response = await fetch(`${API_URL}/api/v1/auth/signup`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(userData),
  });

  if (!response.ok) {
    const error = await response.json();
    const errorMessage = error.detail || error.error?.message || 'Signup failed';
    throw new Error(errorMessage);
  }

  const data: AuthResponse = await response.json();
  setAuthTokens(data);
  return data;
}

/**
 * Logout user
 */
export async function logout(): Promise<void> {
  try {
    // Call logout endpoint (optional, for server-side tracking)
    await fetch(`${API_URL}/api/v1/auth/logout`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });
  } catch (error) {
    console.error('Logout endpoint call failed:', error);
  } finally {
    // Always clear local tokens
    clearAuthTokens();
  }
}

/**
 * React hook for authentication state and methods
 */
export function useAuth() {
  const [user, setUser] = useState<User | null>(inMemoryTokens.user);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // Sync user state with inMemoryTokens
  useEffect(() => {
    setUser(inMemoryTokens.user);
  }, []);

  // Login handler
  const handleLogin = useCallback(async (credentials: LoginRequest) => {
    setLoading(true);
    setError(null);
    try {
      const response = await login(credentials);
      if (response.data?.user) {
        setUser(response.data.user);
      }
      return response;
    } catch (e) {
      const message = e instanceof Error ? e.message : 'Login failed';
      setError(message);
      throw new Error(message);
    } finally {
      setLoading(false);
    }
  }, []);

  // Signup handler
  const handleSignup = useCallback(async (userData: SignupRequest) => {
    setLoading(true);
    setError(null);
    try {
      const response = await signup(userData);
      if (response.data?.user) {
        setUser(response.data.user);
      }
      return response;
    } catch (e) {
      const message = e instanceof Error ? e.message : 'Signup failed';
      setError(message);
      throw new Error(message);
    } finally {
      setLoading(false);
    }
  }, []);

  // Logout handler
  const handleLogout = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      await logout();
      setUser(null);
    } catch (e) {
      const message = e instanceof Error ? e.message : 'Logout failed';
      setError(message);
      throw new Error(message);
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    user,
    loading,
    error,
    login: handleLogin,
    signup: handleSignup,
    logout: handleLogout,
    isAuthenticated: !!user,
  };
}

/**
 * React hook for session state (simplified version)
 */
export function useSession() {
  const { user, isAuthenticated, loading } = useAuth();

  return {
    session: user ? {
      user,
      accessToken: getAccessToken(),
      refreshToken: getRefreshToken(),
    } : null,
    isAuthenticated,
    loading,
  };
}

// Initialize auth on module load
if (typeof window !== 'undefined') {
  initializeAuth();
}
