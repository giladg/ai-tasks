export type Priority = 'low' | 'medium' | 'high' | 'urgent';
export type SourceType = 'gmail' | 'calendar';

export interface Task {
  id: number;
  user_id: number;
  description: string;
  priority: Priority;
  due_date: string | null;
  source_type: SourceType;
  source_link: string | null;
  source_id: string | null;
  extracted_at: string;
  is_done: boolean;
  is_ai_error: boolean;
  created_at: string;
  updated_at: string;
}

export interface TaskUpdate {
  description?: string;
  priority?: Priority;
  due_date?: string | null;
  is_done?: boolean;
  is_ai_error?: boolean;
}

export interface TaskList {
  tasks: Task[];
  total: number;
}

export interface TaskFilters {
  date?: string;
  is_done?: boolean;
  is_ai_error?: boolean;
  priority?: Priority;
  source_type?: SourceType;
}
