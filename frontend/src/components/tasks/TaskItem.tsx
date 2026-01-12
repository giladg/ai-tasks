import React from 'react';
import { Task, Priority } from '../../types/task';
import { formatDate, getPriorityColor } from '../../lib/utils';

interface TaskItemProps {
  task: Task;
  onUpdate: (id: number, update: any) => void;
  onDelete: (id: number) => void;
}

const TaskItem: React.FC<TaskItemProps> = ({ task, onUpdate, onDelete }) => {
  const handlePriorityChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    onUpdate(task.id, { priority: e.target.value as Priority });
  };

  const handleToggleDone = () => {
    onUpdate(task.id, { is_done: !task.is_done });
  };

  const handleMarkAsError = () => {
    onUpdate(task.id, { is_ai_error: !task.is_ai_error });
  };

  return (
    <div
      className={`bg-white border rounded-lg p-4 shadow-sm hover:shadow-md transition-shadow ${
        task.is_done ? 'opacity-60' : ''
      } ${task.is_ai_error ? 'border-red-300 bg-red-50' : 'border-gray-200'}`}
    >
      <div className="flex items-start gap-3">
        {/* Checkbox */}
        <input
          type="checkbox"
          checked={task.is_done}
          onChange={handleToggleDone}
          className="mt-1 w-5 h-5 text-blue-600 rounded focus:ring-2 focus:ring-blue-500"
          disabled={task.is_ai_error}
        />

        {/* Task Content */}
        <div className="flex-1 min-w-0">
          <p
            className={`text-gray-900 mb-2 ${
              task.is_done ? 'line-through text-gray-500' : ''
            }`}
          >
            {task.description}
          </p>

          {/* Metadata */}
          <div className="flex flex-wrap items-center gap-3 text-sm">
            {/* Priority Selector */}
            <select
              value={task.priority}
              onChange={handlePriorityChange}
              disabled={task.is_ai_error}
              className={`px-2 py-1 rounded border text-xs font-medium ${getPriorityColor(
                task.priority
              )}`}
            >
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
              <option value="urgent">Urgent</option>
            </select>

            {/* Due Date */}
            {task.due_date && (
              <span className="text-gray-600 flex items-center gap-1">
                <svg
                  className="w-4 h-4"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
                  />
                </svg>
                {formatDate(task.due_date)}
              </span>
            )}

            {/* Source Type */}
            <span
              className={`px-2 py-1 rounded text-xs font-medium ${
                task.source_type === 'gmail'
                  ? 'bg-purple-50 text-purple-700'
                  : 'bg-green-50 text-green-700'
              }`}
            >
              {task.source_type === 'gmail' ? '📧 Gmail' : '📅 Calendar'}
            </span>

            {/* Source Link */}
            {task.source_link && (
              <a
                href={task.source_link}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-600 hover:text-blue-800 flex items-center gap-1"
              >
                <svg
                  className="w-4 h-4"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
                  />
                </svg>
                View source
              </a>
            )}
          </div>

          {/* AI Error Badge */}
          {task.is_ai_error && (
            <div className="mt-2 text-xs text-red-600 font-medium">
              ⚠️ Marked as not a task
            </div>
          )}
        </div>

        {/* Actions */}
        <div className="flex items-center gap-2">
          <button
            onClick={handleMarkAsError}
            className={`p-2 rounded-lg transition-colors ${
              task.is_ai_error
                ? 'bg-red-100 text-red-600 hover:bg-red-200'
                : 'text-gray-400 hover:text-red-600 hover:bg-red-50'
            }`}
            title={task.is_ai_error ? 'Unmark as error' : 'Mark as AI error'}
          >
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
                d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
          </button>

          <button
            onClick={() => onDelete(task.id)}
            className="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
            title="Delete task"
          >
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
                d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
              />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
};

export default TaskItem;
