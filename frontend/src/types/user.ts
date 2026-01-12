export interface User {
  id: number;
  google_id: string;
  email: string;
  name: string | null;
  picture_url: string | null;
  last_sync_at: string | null;
  is_active: boolean;
  created_at: string;
}

export interface UserProfile extends User {
  updated_at: string;
}
