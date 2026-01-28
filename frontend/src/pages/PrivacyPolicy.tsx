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

        <div className="bg-white rounded-lg shadow-sm p-8 md:p-12 prose prose-blue max-w-none">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Privacy Policy</h1>
          <p className="text-gray-600 text-sm mb-8">Last Updated: January 28, 2026</p>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">Introduction</h2>
            <p className="text-gray-700 leading-relaxed">
              AI Task Manager ("we," "our," or "us") operates ai-tasks.app (the "Service").
              This Privacy Policy explains how we collect, use, disclose, and safeguard your
              information when you use our Service.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">Information We Collect</h2>

            <div className="mb-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-3">Information You Provide</h3>
              <p className="text-gray-700 mb-2">When you sign in with Google, we collect:</p>
              <ul className="list-disc pl-6 space-y-1 text-gray-700">
                <li>Email address</li>
                <li>Name</li>
                <li>Profile picture URL</li>
                <li>Google user ID</li>
              </ul>
            </div>

            <div className="mb-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-3">Information We Access (With Your Permission)</h3>
              <p className="text-gray-700 mb-3">When you authorize access, we access the following data:</p>

              <div className="mb-4">
                <h4 className="text-lg font-semibold text-gray-800 mb-2">Gmail Data</h4>
                <p className="text-gray-700 mb-2">We read your Gmail messages to extract task-related information, including:</p>
                <ul className="list-disc pl-6 space-y-1 text-gray-700 mb-2">
                  <li>Subject lines</li>
                  <li>Email body content</li>
                  <li>Sender information</li>
                  <li>Dates and times</li>
                </ul>
                <p className="text-gray-700 font-medium">
                  <strong>Important:</strong> We do NOT access attachments, spam, trash, or deleted emails.
                </p>
              </div>

              <div className="mb-4">
                <h4 className="text-lg font-semibold text-gray-800 mb-2">Google Calendar Data</h4>
                <p className="text-gray-700 mb-2">We read your calendar events to extract tasks, including:</p>
                <ul className="list-disc pl-6 space-y-1 text-gray-700 mb-2">
                  <li>Event titles</li>
                  <li>Event descriptions</li>
                  <li>Event dates and times</li>
                  <li>Event locations</li>
                </ul>
                <p className="text-gray-700 font-medium">
                  <strong>Important:</strong> We do NOT modify or delete any calendar events.
                </p>
              </div>
            </div>

            <div className="mb-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-3">Data We Generate</h3>
              <p className="text-gray-700 mb-2">From your emails and calendar, we generate the following task information:</p>
              <ul className="list-disc pl-6 space-y-1 text-gray-700">
                <li>Task titles</li>
                <li>Task descriptions</li>
                <li>Due dates</li>
                <li>Priority levels</li>
                <li>Completion status</li>
              </ul>
            </div>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">How We Use Your Information</h2>
            <p className="text-gray-700 mb-3">We use your information for the following purposes:</p>
            <ol className="list-decimal pl-6 space-y-2 text-gray-700">
              <li>
                <strong>Provide the Service:</strong> Extract tasks from your Gmail and Calendar using AI technology.
              </li>
              <li>
                <strong>Authenticate You:</strong> Verify your identity when you log in to the Service.
              </li>
              <li>
                <strong>Sync Your Data:</strong> Automatically update tasks based on new emails and calendar events.
              </li>
              <li>
                <strong>Improve the Service:</strong> Analyze usage patterns in aggregate, anonymized form to enhance functionality.
              </li>
            </ol>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">How We Store Your Information</h2>

            <div className="mb-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-3">Security Measures</h3>
              <p className="text-gray-700 mb-2">We implement the following security measures to protect your data:</p>
              <ul className="list-disc pl-6 space-y-1 text-gray-700">
                <li>
                  <strong>Encryption:</strong> OAuth tokens are encrypted at rest using Fernet encryption.
                </li>
                <li>
                  <strong>Secure Transport:</strong> All data transmission uses HTTPS/TLS encryption.
                </li>
                <li>
                  <strong>Access Control:</strong> Database access is restricted and requires authentication.
                </li>
              </ul>
            </div>

            <div className="mb-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-3">Data Storage</h3>
              <ul className="list-disc pl-6 space-y-1 text-gray-700">
                <li>
                  <strong>OAuth Tokens:</strong> Encrypted and stored in our secure database.
                </li>
                <li>
                  <strong>Tasks:</strong> Stored in our database with user association.
                </li>
                <li>
                  <strong>Emails/Calendar Events:</strong> NOT stored—only processed transiently for task extraction.
                </li>
              </ul>
            </div>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">Third-Party Services</h2>

            <div className="mb-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-3">Google APIs</h3>
              <p className="text-gray-700">
                We use Google OAuth 2.0 and Google APIs to access your Gmail and Calendar data.
                Your use of these services is also governed by{' '}
                <a
                  href="https://policies.google.com/privacy"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:text-blue-800 underline"
                >
                  Google's Privacy Policy
                </a>.
              </p>
            </div>

            <div className="mb-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-3">AI Processing</h3>
              <p className="text-gray-700">
                We use Google's Gemini AI to process your email and calendar content for task extraction.
                This processing happens in real-time during sync and does not permanently store your
                email or calendar content in Gemini systems.
              </p>
            </div>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">Data Retention</h2>
            <ul className="list-disc pl-6 space-y-1 text-gray-700">
              <li>
                <strong>OAuth Tokens:</strong> Retained while your account is active.
              </li>
              <li>
                <strong>Tasks:</strong> Retained while your account is active.
              </li>
              <li>
                <strong>Email/Calendar Content:</strong> NOT retained—processed transiently only.
              </li>
              <li>
                <strong>Account Data:</strong> Retained until you request account deletion.
              </li>
            </ul>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">Your Rights and Choices</h2>

            <div className="mb-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-3">Revoking Access</h3>
              <p className="text-gray-700 mb-2">To revoke our access to your Gmail and Calendar:</p>
              <ol className="list-decimal pl-6 space-y-1 text-gray-700">
                <li>
                  Visit{' '}
                  <a
                    href="https://myaccount.google.com/permissions"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-600 hover:text-blue-800 underline"
                  >
                    Google Account Permissions
                  </a>.
                </li>
                <li>Find "AI Task Manager" in the list of connected apps.</li>
                <li>Click "Remove Access" to revoke permissions.</li>
              </ol>
            </div>

            <div className="mb-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-3">Data Deletion</h3>
              <p className="text-gray-700">
                To delete your account and all associated data, please contact us or use the account
                deletion feature in your dashboard. We will delete all your data within 30 days of your request.
              </p>
            </div>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">Data Sharing</h2>
            <p className="text-gray-700 mb-2">We do NOT:</p>
            <ul className="list-disc pl-6 space-y-1 text-gray-700">
              <li>Sell your data to third parties.</li>
              <li>Share your data with advertisers.</li>
              <li>Use your data for purposes other than providing the Service.</li>
            </ul>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">Contact Us</h2>
            <p className="text-gray-700 mb-3">If you have questions about this Privacy Policy or our data practices:</p>
            <div className="text-gray-700">
              <p className="mb-1">
                <strong>Email:</strong>{' '}
                <a href="mailto:giladgolan3@gmail.com" className="text-blue-600 hover:text-blue-800">
                  giladgolan3@gmail.com
                </a>
              </p>
              <p>
                <strong>Website:</strong>{' '}
                <a href="https://ai-tasks.app" className="text-blue-600 hover:text-blue-800">
                  https://ai-tasks.app
                </a>
              </p>
            </div>
          </section>

          <section className="mb-8 border-t pt-6">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">Google API Services User Data Policy</h2>
            <p className="text-gray-700 mb-3">
              AI Task Manager's use and transfer of information received from Google APIs adheres to the{' '}
              <a
                href="https://developers.google.com/terms/api-services-user-data-policy"
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-600 hover:text-blue-800 underline"
              >
                Google API Services User Data Policy
              </a>, including the Limited Use requirements.
            </p>
            <p className="text-gray-700 mb-2">Specifically:</p>
            <ul className="list-disc pl-6 space-y-1 text-gray-700">
              <li>We only use Gmail and Calendar data to extract tasks for you.</li>
              <li>We do not transfer this data to third parties (except as required to provide the Service).</li>
              <li>We do not use this data for serving advertisements.</li>
              <li>We do not use this data for purposes unrelated to task extraction.</li>
            </ul>
          </section>
        </div>
      </div>
    </div>
  );
};

export default PrivacyPolicy;
