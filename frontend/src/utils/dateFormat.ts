/**
 * Format a date string into a human-readable localized format
 * @param dateString ISO date string from backend (UTC)
 * @returns Formatted date string in local timezone
 */
export const formatDateTime = (dateString: string): string => {
  // Parse the date string - if it doesn't have timezone info, treat as UTC
  let date: Date;

  if (dateString.endsWith('Z') || dateString.includes('+') || dateString.includes('T')) {
    // Has timezone info, parse directly
    date = new Date(dateString);
  } else {
    // No timezone info, append Z to treat as UTC
    date = new Date(dateString + 'Z');
  }

  // Check if date is valid
  if (isNaN(date.getTime())) {
    return 'Invalid date';
  }

  // toLocaleString automatically converts to local timezone
  return date.toLocaleString(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
    hour12: true,
  });
};

/**
 * Format a date as relative time (e.g., "2 minutes ago", "3 hours ago")
 * Falls back to absolute time for dates older than 7 days
 * @param dateString ISO date string from backend (UTC)
 * @returns Relative time string in local timezone
 */
export const formatRelativeTime = (dateString: string): string => {
  // Parse the date string - if it doesn't have timezone info, treat as UTC
  let date: Date;

  if (dateString.endsWith('Z') || dateString.includes('+') || dateString.includes('T')) {
    // Has timezone info, parse directly
    date = new Date(dateString);
  } else {
    // No timezone info, append Z to treat as UTC
    date = new Date(dateString + 'Z');
  }

  const now = new Date();

  // Check if date is valid
  if (isNaN(date.getTime())) {
    return 'Invalid date';
  }

  const diffMs = now.getTime() - date.getTime();
  const diffMinutes = Math.floor(diffMs / (1000 * 60));
  const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

  // Future dates
  if (diffMs < 0) {
    return formatDateTime(dateString);
  }

  // Less than 1 minute
  if (diffMinutes < 1) {
    return 'Just now';
  }

  // Less than 1 hour
  if (diffMinutes < 60) {
    return `${diffMinutes} ${diffMinutes === 1 ? 'minute' : 'minutes'} ago`;
  }

  // Less than 24 hours
  if (diffHours < 24) {
    return `${diffHours} ${diffHours === 1 ? 'hour' : 'hours'} ago`;
  }

  // Less than 7 days - show relative days
  if (diffDays < 7) {
    return `${diffDays} ${diffDays === 1 ? 'day' : 'days'} ago`;
  }

  // Older than 7 days - show absolute date in local timezone
  return formatDateTime(dateString);
};
