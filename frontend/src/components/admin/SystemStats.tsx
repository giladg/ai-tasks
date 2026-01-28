import React from 'react';
import { SystemStats as SystemStatsType } from '../../types/admin';

interface SystemStatsProps {
  stats: SystemStatsType;
}

const SystemStats: React.FC<SystemStatsProps> = ({ stats }) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
      {/* User Stats */}
      <div className="bg-white p-6 rounded-lg shadow">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-sm font-medium text-gray-600">Total Users</h3>
          <svg className="w-5 h-5 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
            <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z" />
          </svg>
        </div>
        <p className="text-3xl font-bold text-gray-900">{stats.total_users}</p>
        <p className="text-sm text-gray-500 mt-1">
          {stats.active_users} active, {stats.admin_users} admins
        </p>
      </div>

      <div className="bg-white p-6 rounded-lg shadow">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-sm font-medium text-gray-600">Data Access</h3>
          <svg className="w-5 h-5 text-green-600" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clipRule="evenodd" />
          </svg>
        </div>
        <p className="text-3xl font-bold text-gray-900">{stats.users_with_data_access}</p>
        <p className="text-sm text-gray-500 mt-1">
          {Math.round((stats.users_with_data_access / Math.max(stats.total_users, 1)) * 100)}% authorized
        </p>
      </div>

      {/* Task Stats */}
      <div className="bg-white p-6 rounded-lg shadow">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-sm font-medium text-gray-600">Total Tasks</h3>
          <svg className="w-5 h-5 text-purple-600" fill="currentColor" viewBox="0 0 20 20">
            <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
            <path fillRule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clipRule="evenodd" />
          </svg>
        </div>
        <p className="text-3xl font-bold text-gray-900">{stats.total_tasks}</p>
        <p className="text-sm text-gray-500 mt-1">
          {stats.pending_tasks} pending, {stats.completed_tasks} completed
        </p>
      </div>

      <div className="bg-white p-6 rounded-lg shadow">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-sm font-medium text-gray-600">Activity</h3>
          <svg className="w-5 h-5 text-orange-600" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clipRule="evenodd" />
          </svg>
        </div>
        <p className="text-3xl font-bold text-gray-900">{stats.tasks_created_today}</p>
        <p className="text-sm text-gray-500 mt-1">
          {stats.tasks_created_this_week} this week
        </p>
      </div>
    </div>
  );
};

export default SystemStats;
