import api from './api';
import { User } from '../types/user';

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface GoogleAuthURL {
  authorization_url: string;
}

export interface AuthStatus {
  authenticated: boolean;
  has_data_access: boolean;
  email: string;
  name: string | null;
}

export const authService = {
  // Get Google OAuth authorization URL
  async getGoogleAuthUrl(): Promise<string> {
    const response = await api.get<GoogleAuthURL>('/api/v1/auth/google/login');
    return response.data.authorization_url;
  },

  // Handle OAuth callback (exchange code for token)
  async handleCallback(code: string, state: string): Promise<AuthResponse> {
    const response = await api.get<AuthResponse>('/api/v1/auth/google/callback', {
      params: { code, state },
    });
    return response.data;
  },

  // Get current user info
  async getCurrentUser(): Promise<User> {
    const response = await api.get<User>('/api/v1/auth/me');
    return response.data;
  },

  // Get authorization status (check if user has Gmail/Calendar access)
  async getAuthStatus(): Promise<AuthStatus> {
    const response = await api.get<AuthStatus>('/api/v1/auth/status');
    return response.data;
  },

  // Get authorization URL for Gmail/Calendar data access
  async authorizeDataAccess(): Promise<GoogleAuthURL> {
    const response = await api.get<GoogleAuthURL>('/api/v1/auth/google/authorize-data');
    return response.data;
  },

  // Logout
  async logout(): Promise<void> {
    await api.post('/api/v1/auth/logout');
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
  },

  // Save auth data to localStorage
  saveAuth(authData: AuthResponse): void {
    localStorage.setItem('access_token', authData.access_token);
    localStorage.setItem('user', JSON.stringify(authData.user));
  },

  // Get saved user from localStorage
  getSavedUser(): User | null {
    const userStr = localStorage.getItem('user');
    if (userStr) {
      try {
        return JSON.parse(userStr);
      } catch {
        return null;
      }
    }
    return null;
  },

  // Check if user is authenticated
  isAuthenticated(): boolean {
    return !!localStorage.getItem('access_token');
  },
};
