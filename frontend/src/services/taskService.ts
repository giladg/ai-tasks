import api from './api';
import { Task, TaskUpdate, TaskList, TaskFilters } from '../types/task';

export const taskService = {
  // Get all tasks with optional filters
  async getTasks(filters?: TaskFilters): Promise<TaskList> {
    const response = await api.get<TaskList>('/api/v1/tasks', {
      params: filters,
    });
    return response.data;
  },

  // Get single task by ID
  async getTask(id: number): Promise<Task> {
    const response = await api.get<Task>(`/api/v1/tasks/${id}`);
    return response.data;
  },

  // Update task
  async updateTask(id: number, update: TaskUpdate): Promise<Task> {
    const response = await api.patch<Task>(`/api/v1/tasks/${id}`, update);
    return response.data;
  },

  // Delete task
  async deleteTask(id: number): Promise<void> {
    await api.delete(`/api/v1/tasks/${id}`);
  },

  // Trigger manual sync
  async triggerSync(): Promise<void> {
    await api.post('/api/v1/tasks/trigger-sync');
  },

  // Get available extraction dates
  async getExtractionDates(): Promise<string[]> {
    const response = await api.get<string[]>('/api/v1/tasks/extraction-dates');
    return response.data;
  },
};
