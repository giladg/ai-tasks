export interface UserListItem {
  id: number;
  email: string;
  name: string | null;
  is_active: boolean;
  is_admin: boolean;
  has_data_access: boolean;
  task_count: number;
  last_sync_at: string | null;
  created_at: string;
}

export interface UserDetail {
  id: number;
  email: string;
  name: string | null;
  picture_url: string | null;
  is_active: boolean;
  is_admin: boolean;
  has_data_access: boolean;
  last_sync_at: string | null;
  created_at: string;
  updated_at: string;
  task_count: number;
  pending_tasks: number;
  completed_tasks: number;
}

export interface UserUpdate {
  is_active?: boolean;
  is_admin?: boolean;
}

export interface SystemStats {
  total_users: number;
  active_users: number;
  admin_users: number;
  users_with_data_access: number;
  total_tasks: number;
  pending_tasks: number;
  completed_tasks: number;
  tasks_created_today: number;
  tasks_created_this_week: number;
}
