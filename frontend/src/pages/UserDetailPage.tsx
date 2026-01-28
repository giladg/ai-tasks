import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { adminService } from '../services/adminService';

const UserDetailPage: React.FC = () => {
  const { userId } = useParams<{ userId: string }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  // Fetch user details
  const { data: user, isLoading } = useQuery({
    queryKey: ['admin-user', userId],
    queryFn: () => adminService.getUserDetail(Number(userId)),
    enabled: !!userId,
  });

  // Toggle active status
  const toggleActiveMutation = useMutation({
    mutationFn: (isActive: boolean) =>
      adminService.updateUser(Number(userId), { is_active: isActive }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['admin-user', userId] });
      queryClient.invalidateQueries({ queryKey: ['admin-users'] });
      queryClient.invalidateQueries({ queryKey: ['admin-stats'] });
    },
  });

  // Toggle admin status
  const toggleAdminMutation = useMutation({
    mutationFn: (isAdmin: boolean) =>
      adminService.updateUser(Number(userId), { is_admin: isAdmin }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['admin-user', userId] });
      queryClient.invalidateQueries({ queryKey: ['admin-users'] });
      queryClient.invalidateQueries({ queryKey: ['admin-stats'] });
    },
  });

  // Trigger sync
  const syncMutation = useMutation({
    mutationFn: () => adminService.triggerUserSync(Number(userId)),
  });

  // Delete user
  const deleteMutation = useMutation({
    mutationFn: () => adminService.deleteUser(Number(userId)),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['admin-users'] });
      queryClient.invalidateQueries({ queryKey: ['admin-stats'] });
      navigate('/admin');
    },
  });

  const formatDate = (dateString: string | null) => {
    if (!dateString) return 'Never';
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">User not found</h2>
          <button
            onClick={() => navigate('/admin')}
            className="text-blue-600 hover:text-blue-800"
          >
            Back to Admin Dashboard
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header with back button */}
        <div className="mb-6">
          <button
            onClick={() => navigate('/admin')}
            className="flex items-center text-blue-600 hover:text-blue-800 mb-4"
          >
            <svg className="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            Back to Admin Dashboard
          </button>
          <h1 className="text-3xl font-bold text-gray-900">User Details</h1>
        </div>

        {/* User Info Card */}
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <div className="flex items-start justify-between mb-6">
            <div className="flex items-center gap-4">
              {user.picture_url && (
                <img
                  src={user.picture_url}
                  alt={user.name || user.email}
                  className="w-16 h-16 rounded-full"
                />
              )}
              <div>
                <h2 className="text-2xl font-bold text-gray-900">{user.name || 'No name'}</h2>
                <p className="text-gray-600">{user.email}</p>
                <div className="flex gap-2 mt-2">
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                    user.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                  }`}>
                    {user.is_active ? 'Active' : 'Inactive'}
                  </span>
                  {user.is_admin && (
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                      Admin
                    </span>
                  )}
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                    user.has_data_access ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-800'
                  }`}>
                    {user.has_data_access ? 'Data Access' : 'No Data Access'}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4 border-t pt-4">
            <div>
              <p className="text-sm text-gray-600">User ID</p>
              <p className="font-medium">{user.id}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Created</p>
              <p className="font-medium">{formatDate(user.created_at)}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Last Updated</p>
              <p className="font-medium">{formatDate(user.updated_at)}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Last Sync</p>
              <p className="font-medium">{formatDate(user.last_sync_at)}</p>
            </div>
          </div>
        </div>

        {/* Task Stats */}
        <div className="grid grid-cols-3 gap-4 mb-6">
          <div className="bg-white rounded-lg shadow p-6">
            <p className="text-sm text-gray-600 mb-1">Total Tasks</p>
            <p className="text-3xl font-bold text-gray-900">{user.task_count}</p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <p className="text-sm text-gray-600 mb-1">Pending Tasks</p>
            <p className="text-3xl font-bold text-orange-600">{user.pending_tasks}</p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <p className="text-sm text-gray-600 mb-1">Completed Tasks</p>
            <p className="text-3xl font-bold text-green-600">{user.completed_tasks}</p>
          </div>
        </div>

        {/* Actions */}
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Actions</h3>
          <div className="space-y-3">
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div>
                <p className="font-medium text-gray-900">Account Status</p>
                <p className="text-sm text-gray-600">
                  {user.is_active ? 'Deactivate user account' : 'Activate user account'}
                </p>
              </div>
              <button
                onClick={() => toggleActiveMutation.mutate(!user.is_active)}
                disabled={toggleActiveMutation.isPending}
                className={`px-4 py-2 rounded-md font-medium transition-colors ${
                  user.is_active
                    ? 'bg-red-600 text-white hover:bg-red-700'
                    : 'bg-green-600 text-white hover:bg-green-700'
                } disabled:bg-gray-400`}
              >
                {toggleActiveMutation.isPending ? 'Updating...' : user.is_active ? 'Deactivate' : 'Activate'}
              </button>
            </div>

            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div>
                <p className="font-medium text-gray-900">Admin Access</p>
                <p className="text-sm text-gray-600">
                  {user.is_admin ? 'Revoke admin privileges' : 'Grant admin privileges'}
                </p>
              </div>
              <button
                onClick={() => toggleAdminMutation.mutate(!user.is_admin)}
                disabled={toggleAdminMutation.isPending}
                className={`px-4 py-2 rounded-md font-medium transition-colors ${
                  user.is_admin
                    ? 'bg-orange-600 text-white hover:bg-orange-700'
                    : 'bg-purple-600 text-white hover:bg-purple-700'
                } disabled:bg-gray-400`}
              >
                {toggleAdminMutation.isPending ? 'Updating...' : user.is_admin ? 'Revoke Admin' : 'Make Admin'}
              </button>
            </div>

            {user.has_data_access && (
              <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div>
                  <p className="font-medium text-gray-900">Manual Sync</p>
                  <p className="text-sm text-gray-600">Trigger immediate sync for this user</p>
                </div>
                <button
                  onClick={() => syncMutation.mutate()}
                  disabled={syncMutation.isPending}
                  className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 font-medium transition-colors disabled:bg-gray-400"
                >
                  {syncMutation.isPending ? 'Syncing...' : 'Sync Now'}
                </button>
              </div>
            )}

            {syncMutation.isSuccess && (
              <div className="p-3 bg-green-50 border border-green-200 rounded-lg text-green-800">
                Sync queued successfully
              </div>
            )}
          </div>
        </div>

        {/* Danger Zone */}
        <div className="bg-white rounded-lg shadow p-6 border-2 border-red-200">
          <h3 className="text-lg font-semibold text-red-900 mb-4">Danger Zone</h3>
          {!showDeleteConfirm ? (
            <div className="flex items-center justify-between">
              <div>
                <p className="font-medium text-gray-900">Delete User</p>
                <p className="text-sm text-gray-600">Permanently delete this user and all their data</p>
              </div>
              <button
                onClick={() => setShowDeleteConfirm(true)}
                className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 font-medium transition-colors"
              >
                Delete User
              </button>
            </div>
          ) : (
            <div className="space-y-3">
              <p className="text-red-900 font-medium">
                Are you sure you want to delete this user? This action cannot be undone.
              </p>
              <div className="flex gap-3">
                <button
                  onClick={() => deleteMutation.mutate()}
                  disabled={deleteMutation.isPending}
                  className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 font-medium transition-colors disabled:bg-gray-400"
                >
                  {deleteMutation.isPending ? 'Deleting...' : 'Yes, Delete User'}
                </button>
                <button
                  onClick={() => setShowDeleteConfirm(false)}
                  disabled={deleteMutation.isPending}
                  className="px-4 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300 font-medium transition-colors"
                >
                  Cancel
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default UserDetailPage;
