import React, { useState } from 'react';
import { useTasks } from '../hooks/useTasks';
import { useAuth } from '../context/AuthContext';
import TaskList from '../components/tasks/TaskList';
import TaskFilters from '../components/tasks/TaskFilters';
import { Priority, SourceType } from '../types/task';

const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const [filters, setFilters] = useState<{
    is_done?: boolean;
    priority?: Priority;
    source_type?: SourceType;
  }>({
    is_done: false, // Show only pending tasks by default
  });

  const {
    tasks,
    total,
    isLoading,
    updateTask,
    deleteTask,
    triggerSync,
    isSyncing,
  } = useTasks(filters);

  const handleSync = () => {
    triggerSync();
  };

  // Calculate stats
  const pendingCount = tasks.filter(t => !t.is_done && !t.is_ai_error).length;
  const urgentCount = tasks.filter(t => t.priority === 'urgent' && !t.is_done).length;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">My Tasks</h1>
              <p className="text-sm text-gray-600 mt-1">
                Welcome back, {user?.name || user?.email}
              </p>
            </div>
            <button
              onClick={handleSync}
              disabled={isSyncing}
              className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
            >
              {isSyncing ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  <span>Syncing...</span>
                </>
              ) : (
                <>
                  <svg
                    className="w-5 h-5"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                    />
                  </svg>
                  <span>Sync Now</span>
                </>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white border border-gray-200 rounded-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 mb-1">Total Tasks</p>
                <p className="text-3xl font-bold text-gray-900">{total}</p>
              </div>
              <div className="bg-blue-100 p-3 rounded-lg">
                <svg
                  className="w-8 h-8 text-blue-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
                  />
                </svg>
              </div>
            </div>
          </div>

          <div className="bg-white border border-gray-200 rounded-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 mb-1">Pending</p>
                <p className="text-3xl font-bold text-gray-900">{pendingCount}</p>
              </div>
              <div className="bg-orange-100 p-3 rounded-lg">
                <svg
                  className="w-8 h-8 text-orange-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>
            </div>
          </div>

          <div className="bg-white border border-gray-200 rounded-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 mb-1">Urgent</p>
                <p className="text-3xl font-bold text-gray-900">{urgentCount}</p>
              </div>
              <div className="bg-red-100 p-3 rounded-lg">
                <svg
                  className="w-8 h-8 text-red-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                  />
                </svg>
              </div>
            </div>
          </div>
        </div>

        {/* Last Sync Info */}
        {user?.last_sync_at && (
          <div className="mb-6 text-sm text-gray-600">
            Last synced: {new Date(user.last_sync_at).toLocaleString()}
          </div>
        )}

        {/* Filters */}
        <TaskFilters filters={filters} onFilterChange={setFilters} />

        {/* Task List */}
        <TaskList
          tasks={tasks}
          onUpdate={updateTask}
          onDelete={deleteTask}
          isLoading={isLoading}
        />
      </div>
    </div>
  );
};

export default Dashboard;
