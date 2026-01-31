/**
 * Parse UTC datetime string from backend into local Date object
 * Backend sends datetime in format: "2026-01-31T12:34:56.123456" (no timezone, but it's UTC)
 * @param dateString ISO date string from backend (assumed UTC if no timezone)
 * @returns Date object in local timezone
 */
const parseUTCDate = (dateString: string): Date => {
  // If already has timezone info (Z or +/-), parse directly
  if (dateString.endsWith('Z') || /[+-]\d{2}:\d{2}$/.test(dateString)) {
    return new Date(dateString);
  }

  // Backend sends naive datetime (no timezone) - treat as UTC
  // Append 'Z' to explicitly mark as UTC
  return new Date(dateString + 'Z');
};

/**
 * Format a date string into a human-readable localized format
 * @param dateString ISO date string from backend (UTC)
 * @returns Formatted date string in local timezone
 */
export const formatDateTime = (dateString: string): string => {
  const date = parseUTCDate(dateString);

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
  const date = parseUTCDate(dateString);
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
