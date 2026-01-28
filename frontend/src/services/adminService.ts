import api from './api';
import { UserListItem, UserDetail, UserUpdate, SystemStats } from '../types/admin';

export interface UserFilters {
  skip?: number;
  limit?: number;
  search?: string;
  is_active?: boolean;
  is_admin?: boolean;
}

export const adminService = {
  // List users with optional filters
  async listUsers(filters?: UserFilters): Promise<UserListItem[]> {
    const response = await api.get<UserListItem[]>('/api/v1/admin/users', {
      params: filters,
    });
    return response.data;
  },

  // Get user details
  async getUserDetail(userId: number): Promise<UserDetail> {
    const response = await api.get<UserDetail>(`/api/v1/admin/users/${userId}`);
    return response.data;
  },

  // Update user
  async updateUser(userId: number, update: UserUpdate): Promise<UserDetail> {
    const response = await api.patch<UserDetail>(`/api/v1/admin/users/${userId}`, update);
    return response.data;
  },

  // Delete user
  async deleteUser(userId: number): Promise<{ message: string }> {
    const response = await api.delete<{ message: string }>(`/api/v1/admin/users/${userId}`);
    return response.data;
  },

  // Trigger user sync
  async triggerUserSync(userId: number): Promise<{ message: string }> {
    const response = await api.post<{ message: string }>(`/api/v1/admin/users/${userId}/sync`);
    return response.data;
  },

  // Get system stats
  async getSystemStats(): Promise<SystemStats> {
    const response = await api.get<SystemStats>('/api/v1/admin/stats');
    return response.data;
  },
};
