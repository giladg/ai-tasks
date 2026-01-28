import React from 'react';
import { Link } from 'react-router-dom';

const PrivacyPolicy: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 py-12">
        <div className="mb-8">
          <Link to="/" className="text-blue-600 hover:text-blue-800">
            ← Back to Home
          </Link>
        </div>

        <div className="bg-white rounded-lg shadow-sm p-8 prose prose-blue max-w-none">
          <h1>Privacy Policy</h1>
          <p className="text-gray-600">Last Updated: January 28, 2026</p>

          <h2>Introduction</h2>
          <p>
            AI Task Manager ("we," "our," or "us") operates ai-tasks.app (the "Service").
            This Privacy Policy explains how we collect, use, disclose, and safeguard your
            information when you use our Service.
          </p>

          <h2>Information We Collect</h2>

          <h3>Information You Provide</h3>
          <p>When you sign in with Google, we collect:</p>
          <ul>
            <li>Email address</li>
            <li>Name</li>
            <li>Profile picture URL</li>
            <li>Google user ID</li>
          </ul>

          <h3>Information We Access (With Your Permission)</h3>
          <p>When you authorize access, we access:</p>

          <p><strong>Gmail Data</strong> - We read your Gmail messages to extract task-related information:</p>
          <ul>
            <li>Subject lines</li>
            <li>Email body content</li>
            <li>Sender information</li>
            <li>Dates and times</li>
            <li>We do NOT access: Attachments, spam, trash, or deleted emails</li>
          </ul>

          <p><strong>Google Calendar Data</strong> - We read your calendar events to extract tasks:</p>
          <ul>
            <li>Event titles</li>
            <li>Event descriptions</li>
            <li>Event dates and times</li>
            <li>Event locations</li>
            <li>We do NOT modify or delete any calendar events</li>
          </ul>

          <h3>Data We Generate</h3>
          <p><strong>Tasks</strong> - Information extracted from your emails and calendar:</p>
          <ul>
            <li>Task titles</li>
            <li>Task descriptions</li>
            <li>Due dates</li>
            <li>Priority levels</li>
            <li>Completion status</li>
          </ul>

          <h2>How We Use Your Information</h2>
          <p>We use your information to:</p>
          <ol>
            <li><strong>Provide the Service</strong>: Extract tasks from your Gmail and Calendar using AI</li>
            <li><strong>Authenticate You</strong>: Verify your identity when you log in</li>
            <li><strong>Sync Your Data</strong>: Automatically update tasks based on new emails and events</li>
            <li><strong>Improve the Service</strong>: Analyze usage patterns (in aggregate, anonymized form)</li>
          </ol>

          <h2>How We Store Your Information</h2>

          <h3>Security Measures</h3>
          <ul>
            <li><strong>Encryption</strong>: OAuth tokens are encrypted at rest using Fernet encryption</li>
            <li><strong>Secure Transport</strong>: All data transmission uses HTTPS/TLS</li>
            <li><strong>Access Control</strong>: Database access is restricted and authenticated</li>
          </ul>

          <h3>Data Storage</h3>
          <ul>
            <li><strong>OAuth Tokens</strong>: Encrypted and stored in our database</li>
            <li><strong>Tasks</strong>: Stored in our database with user association</li>
            <li><strong>Emails/Calendar Events</strong>: NOT stored - only processed transiently for task extraction</li>
          </ul>

          <h2>Third-Party Services</h2>

          <h3>Google APIs</h3>
          <p>
            We use Google OAuth 2.0 and Google APIs to access your Gmail and Calendar data.
            Your use of these services is also governed by{' '}
            <a href="https://policies.google.com/privacy" target="_blank" rel="noopener noreferrer">
              Google's Privacy Policy
            </a>.
          </p>

          <h3>AI Processing</h3>
          <p>
            We use Google's Gemini AI to process your email and calendar content for task extraction.
            This processing happens in real-time during sync and does not permanently store your
            email/calendar content in Gemini systems.
          </p>

          <h2>Data Retention</h2>
          <ul>
            <li><strong>OAuth Tokens</strong>: Retained while your account is active</li>
            <li><strong>Tasks</strong>: Retained while your account is active</li>
            <li><strong>Email/Calendar Content</strong>: NOT retained - processed transiently only</li>
            <li><strong>Account Data</strong>: Retained until account deletion</li>
          </ul>

          <h2>Your Rights and Choices</h2>

          <h3>Revoking Access</h3>
          <p>To revoke our access to Gmail/Calendar:</p>
          <ol>
            <li>Visit{' '}
              <a href="https://myaccount.google.com/permissions" target="_blank" rel="noopener noreferrer">
                Google Account Permissions
              </a>
            </li>
            <li>Find "AI Task Manager"</li>
            <li>Click "Remove Access"</li>
          </ol>

          <h3>Data Deletion</h3>
          <p>
            To delete your account and all associated data, contact us or use the account
            deletion feature in your dashboard. We will delete all your data within 30 days.
          </p>

          <h2>Data Sharing</h2>
          <p>We do NOT:</p>
          <ul>
            <li>Sell your data to third parties</li>
            <li>Share your data with advertisers</li>
            <li>Use your data for purposes other than providing the Service</li>
          </ul>

          <h2>Contact Us</h2>
          <p>If you have questions about this Privacy Policy or our data practices:</p>
          <p>
            <strong>Email</strong>: support@ai-tasks.app<br />
            <strong>Website</strong>: <a href="https://ai-tasks.app">https://ai-tasks.app</a>
          </p>

          <h2>Google API Services User Data Policy</h2>
          <p>
            AI Task Manager's use and transfer of information received from Google APIs adheres to the{' '}
            <a href="https://developers.google.com/terms/api-services-user-data-policy" target="_blank" rel="noopener noreferrer">
              Google API Services User Data Policy
            </a>, including the Limited Use requirements.
          </p>
          <p>Specifically:</p>
          <ul>
            <li>We only use Gmail and Calendar data to extract tasks for you</li>
            <li>We do not transfer this data to third parties (except as required for the Service)</li>
            <li>We do not use this data for serving ads</li>
            <li>We do not use this data for purposes unrelated to task extraction</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default PrivacyPolicy;
