import React from 'react';
import { useExtractionDates } from '../../hooks/useExtractionDates';

interface DateNavigatorProps {
  selectedDate: string | null;
  onDateChange: (date: string | null) => void;
}

const DateNavigator: React.FC<DateNavigatorProps> = ({ selectedDate, onDateChange }) => {
  const { dates, isLoading } = useExtractionDates();

  if (isLoading) {
    return (
      <div className="bg-white rounded-lg shadow-sm p-4 mb-6">
        <div className="animate-pulse">
          <div className="h-4 bg-gray-200 rounded w-32 mb-3"></div>
          <div className="h-10 bg-gray-200 rounded"></div>
        </div>
      </div>
    );
  }

  if (!dates || dates.length === 0) {
    return null;
  }

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    const today = new Date();
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);

    // Compare dates (ignore time)
    const dateOnly = new Date(date.getFullYear(), date.getMonth(), date.getDate());
    const todayOnly = new Date(today.getFullYear(), today.getMonth(), today.getDate());
    const yesterdayOnly = new Date(yesterday.getFullYear(), yesterday.getMonth(), yesterday.getDate());

    if (dateOnly.getTime() === todayOnly.getTime()) {
      return 'Today';
    } else if (dateOnly.getTime() === yesterdayOnly.getTime()) {
      return 'Yesterday';
    } else {
      return date.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: date.getFullYear() !== today.getFullYear() ? 'numeric' : undefined
      });
    }
  };

  // Latest date is shown by default (selectedDate = null)
  const latestDate = dates[0];
  const isLatest = selectedDate === null || selectedDate === latestDate;

  return (
    <div className="bg-white rounded-lg shadow-sm p-4 mb-6">
      <label className="block text-sm font-medium text-gray-700 mb-3">
        View tasks from:
      </label>
      <div className="flex items-center gap-3">
        {/* Latest button */}
        <button
          onClick={() => onDateChange(null)}
          className={`px-4 py-2 rounded-lg font-medium transition-colors ${
            isLatest
              ? 'bg-blue-600 text-white'
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }`}
        >
          Latest
        </button>

        {/* Date selector */}
        <select
          value={selectedDate || latestDate}
          onChange={(e) => onDateChange(e.target.value === latestDate ? null : e.target.value)}
          className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
        >
          {dates.map((date) => (
            <option key={date} value={date}>
              {formatDate(date)}
            </option>
          ))}
        </select>

        {/* Navigation buttons */}
        {dates.length > 1 && (
          <div className="flex gap-2">
            <button
              onClick={() => {
                const currentIndex = selectedDate ? dates.indexOf(selectedDate) : 0;
                const prevIndex = currentIndex - 1;
                if (prevIndex >= 0) {
                  onDateChange(dates[prevIndex]);
                }
              }}
              disabled={isLatest}
              className="p-2 rounded-lg bg-gray-100 text-gray-700 hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              title="Newer"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
            </button>
            <button
              onClick={() => {
                const currentIndex = selectedDate ? dates.indexOf(selectedDate) : 0;
                const nextIndex = currentIndex + 1;
                if (nextIndex < dates.length) {
                  onDateChange(dates[nextIndex]);
                }
              }}
              disabled={selectedDate === dates[dates.length - 1]}
              className="p-2 rounded-lg bg-gray-100 text-gray-700 hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              title="Older"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </button>
          </div>
        )}
      </div>

      {/* Show selected date info */}
      {selectedDate && (
        <p className="text-sm text-gray-500 mt-2">
          Showing tasks extracted on {formatDate(selectedDate)}
        </p>
      )}
    </div>
  );
};

export default DateNavigator;
