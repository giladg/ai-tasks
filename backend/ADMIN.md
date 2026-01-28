# Admin Dashboard

This document describes the admin features available in the AI Task Manager application.

## Overview

The admin dashboard provides tools for managing users and monitoring system activity. Admin users have access to:

- View system statistics (users, tasks, activity)
- List and search all users
- View detailed user information
- Activate/deactivate user accounts
- Grant/revoke admin privileges
- Trigger manual syncs for users
- Delete users and their data

## Making a User Admin

### Using the Command-Line Tool

The easiest way to make a user an admin is using the `make_admin.py` script:

```bash
# Make a user admin
cd backend
python scripts/make_admin.py user@example.com

# Revoke admin privileges
python scripts/make_admin.py user@example.com --revoke

# List all users
python scripts/make_admin.py --list
```

### Manual Database Update

Alternatively, you can update the database directly:

```sql
-- Make a user admin
UPDATE users SET is_admin = 1 WHERE email = 'user@example.com';

-- List all users
SELECT id, email, name, is_admin, is_active FROM users;
```

## Admin Dashboard Features

### System Statistics

The dashboard shows real-time statistics:
- Total users, active users, admin users
- Users with data access authorized
- Total tasks, pending tasks, completed tasks
- Tasks created today and this week

### User Management

#### Listing Users

- View all users in a searchable, filterable table
- Filter by active/inactive status
- Filter by admin/regular user
- Search by name or email
- See task counts and last sync time for each user

#### User Details

Click on any user to see:
- Full profile information
- Task statistics (total, pending, completed)
- Account status and permissions
- Last sync time

#### Available Actions

For each user, admins can:

1. **Activate/Deactivate Account**
   - Inactive users cannot log in
   - Their data is preserved

2. **Grant/Revoke Admin Privileges**
   - Make users admins or remove admin access
   - Cannot remove your own admin privileges

3. **Trigger Manual Sync** (if user has data access)
   - Force an immediate sync of Gmail/Calendar data
   - Useful for testing or troubleshooting

4. **Delete User** (Danger Zone)
   - Permanently deletes user and all their data
   - Cannot be undone
   - Cannot delete your own account
   - Requires confirmation

## API Endpoints

All admin endpoints require authentication and admin privileges.

### List Users
```
GET /api/v1/admin/users
Query params:
  - skip: number (pagination offset)
  - limit: number (pagination limit, max 100)
  - search: string (search name/email)
  - is_active: boolean
  - is_admin: boolean
```

### Get User Details
```
GET /api/v1/admin/users/{user_id}
```

### Update User
```
PATCH /api/v1/admin/users/{user_id}
Body:
  {
    "is_active": boolean,
    "is_admin": boolean
  }
```

### Delete User
```
DELETE /api/v1/admin/users/{user_id}
```

### Trigger User Sync
```
POST /api/v1/admin/users/{user_id}/sync
```

### Get System Stats
```
GET /api/v1/admin/stats
```

## Security

- Admin endpoints are protected by the `get_current_admin_user` dependency
- Non-admin users receive a 403 Forbidden error
- Admins cannot deactivate themselves
- Admins cannot remove their own admin privileges
- Admins cannot delete their own account
- All admin actions are performed with proper authentication checks

## Accessing the Admin Dashboard

1. Log in to the application
2. If you have admin privileges, you'll see an "Admin" link in the navigation
3. Click "Admin" to access the dashboard
4. Non-admin users who try to access `/admin` will see an "Access Denied" message

## Database Migration

The admin feature requires the `add_is_admin_field` migration to be run:

```bash
cd backend
alembic upgrade head
```

This migration:
- Adds `is_admin` boolean column to the `users` table
- Sets all existing users to `is_admin = False`
- Sets the column as non-nullable with default value `False`

## First-Time Setup

1. Run the database migration:
   ```bash
   cd backend
   alembic upgrade head
   ```

2. Create your first admin user:
   ```bash
   python scripts/make_admin.py your-email@example.com
   ```

3. Log in to the application with that user

4. Access the admin dashboard at `/admin`

## Troubleshooting

### "Access Denied" when accessing /admin

- Make sure your user account has `is_admin = True` in the database
- Log out and log back in to refresh your session
- Check that you're logged in with the correct account

### Cannot see Admin link in navigation

- Verify your user has admin privileges: `python scripts/make_admin.py --list`
- Check browser console for JavaScript errors
- Clear browser cache and refresh

### Admin API endpoints return 403

- Verify JWT token is valid and contains admin user info
- Check backend logs for authentication errors
- Ensure `is_admin` field exists in database (run migration if needed)
