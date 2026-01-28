import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { adminService } from '../services/adminService';
import SystemStats from '../components/admin/SystemStats';
import UserListTable from '../components/admin/UserListTable';

const AdminDashboard: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterActive, setFilterActive] = useState<boolean | undefined>(undefined);
  const [filterAdmin, setFilterAdmin] = useState<boolean | undefined>(undefined);

  // Fetch system stats
  const { data: stats, isLoading: statsLoading } = useQuery({
    queryKey: ['admin-stats'],
    queryFn: () => adminService.getSystemStats(),
    refetchInterval: 30000, // Refresh every 30 seconds
  });

  // Fetch users with filters
  const { data: users, isLoading: usersLoading, refetch: refetchUsers } = useQuery({
    queryKey: ['admin-users', searchTerm, filterActive, filterAdmin],
    queryFn: () => adminService.listUsers({
      search: searchTerm || undefined,
      is_active: filterActive,
      is_admin: filterAdmin,
    }),
    refetchInterval: 30000,
  });

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Admin Dashboard</h1>
          <p className="text-gray-600 mt-2">Manage users and monitor system activity</p>
        </div>

        {/* System Stats */}
        {statsLoading ? (
          <div className="flex justify-center items-center h-32">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          </div>
        ) : stats ? (
          <SystemStats stats={stats} />
        ) : null}

        {/* Filters */}
        <div className="bg-white rounded-lg shadow p-4 mb-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label htmlFor="search" className="block text-sm font-medium text-gray-700 mb-1">
                Search
              </label>
              <input
                id="search"
                type="text"
                placeholder="Search by name or email..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label htmlFor="filterActive" className="block text-sm font-medium text-gray-700 mb-1">
                Status
              </label>
              <select
                id="filterActive"
                value={filterActive === undefined ? '' : filterActive.toString()}
                onChange={(e) => setFilterActive(e.target.value === '' ? undefined : e.target.value === 'true')}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">All</option>
                <option value="true">Active</option>
                <option value="false">Inactive</option>
              </select>
            </div>

            <div>
              <label htmlFor="filterAdmin" className="block text-sm font-medium text-gray-700 mb-1">
                Role
              </label>
              <select
                id="filterAdmin"
                value={filterAdmin === undefined ? '' : filterAdmin.toString()}
                onChange={(e) => setFilterAdmin(e.target.value === '' ? undefined : e.target.value === 'true')}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">All</option>
                <option value="true">Admins</option>
                <option value="false">Regular Users</option>
              </select>
            </div>
          </div>
        </div>

        {/* User List */}
        {usersLoading ? (
          <div className="flex justify-center items-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>
        ) : users ? (
          <UserListTable users={users} onRefresh={() => refetchUsers()} />
        ) : null}
      </div>
    </div>
  );
};

export default AdminDashboard;
