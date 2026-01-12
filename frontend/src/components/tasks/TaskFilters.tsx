import React from 'react';
import { Priority, SourceType } from '../../types/task';

interface TaskFiltersProps {
  filters: {
    is_done?: boolean;
    priority?: Priority;
    source_type?: SourceType;
  };
  onFilterChange: (filters: any) => void;
}

const TaskFilters: React.FC<TaskFiltersProps> = ({ filters, onFilterChange }) => {
  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4 mb-6">
      <h3 className="text-sm font-semibold text-gray-700 mb-3">Filters</h3>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Status Filter */}
        <div>
          <label className="block text-xs text-gray-600 mb-1">Status</label>
          <select
            value={filters.is_done === undefined ? 'all' : filters.is_done ? 'done' : 'pending'}
            onChange={(e) => {
              const value = e.target.value;
              onFilterChange({
                ...filters,
                is_done: value === 'all' ? undefined : value === 'done',
              });
            }}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="all">All Tasks</option>
            <option value="pending">Pending</option>
            <option value="done">Done</option>
          </select>
        </div>

        {/* Priority Filter */}
        <div>
          <label className="block text-xs text-gray-600 mb-1">Priority</label>
          <select
            value={filters.priority || 'all'}
            onChange={(e) => {
              const value = e.target.value;
              onFilterChange({
                ...filters,
                priority: value === 'all' ? undefined : value,
              });
            }}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="all">All Priorities</option>
            <option value="urgent">Urgent</option>
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
          </select>
        </div>

        {/* Source Filter */}
        <div>
          <label className="block text-xs text-gray-600 mb-1">Source</label>
          <select
            value={filters.source_type || 'all'}
            onChange={(e) => {
              const value = e.target.value;
              onFilterChange({
                ...filters,
                source_type: value === 'all' ? undefined : value,
              });
            }}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="all">All Sources</option>
            <option value="gmail">Gmail</option>
            <option value="calendar">Calendar</option>
          </select>
        </div>
      </div>

      {/* Clear Filters */}
      {(filters.is_done !== undefined || filters.priority || filters.source_type) && (
        <button
          onClick={() => onFilterChange({})}
          className="mt-3 text-sm text-blue-600 hover:text-blue-800 font-medium"
        >
          Clear all filters
        </button>
      )}
    </div>
  );
};

export default TaskFilters;
