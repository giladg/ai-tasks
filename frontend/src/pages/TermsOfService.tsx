import React from 'react';
import { Link } from 'react-router-dom';

const TermsOfService: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 py-12">
        <div className="mb-8">
          <Link to="/" className="text-blue-600 hover:text-blue-800">
            ← Back to Home
          </Link>
        </div>

        <div className="bg-white rounded-lg shadow-sm p-8 prose prose-blue max-w-none">
          <h1>Terms of Service</h1>
          <p className="text-gray-600">Last Updated: January 28, 2026</p>

          <h2>1. Agreement to Terms</h2>
          <p>
            By accessing or using AI Task Manager ("the Service"), you agree to be bound by these
            Terms of Service ("Terms"). If you do not agree to these Terms, do not use the Service.
          </p>

          <h2>2. Description of Service</h2>
          <p>AI Task Manager is a web-based application that:</p>
          <ul>
            <li>Extracts tasks from your Gmail emails and Google Calendar events</li>
            <li>Uses artificial intelligence to identify and organize tasks</li>
            <li>Provides a dashboard to view, manage, and track tasks</li>
            <li>Syncs automatically with your Gmail and Calendar</li>
          </ul>

          <h2>3. Eligibility</h2>
          <p>
            You must be at least 13 years old to use this Service. By using the Service,
            you represent and warrant that you meet this requirement.
          </p>

          <h2>4. Account Registration</h2>

          <h3>Google Authentication</h3>
          <ul>
            <li>You must sign in with a valid Google account</li>
            <li>You are responsible for maintaining the security of your Google account</li>
            <li>You agree to provide accurate and complete information</li>
          </ul>

          <h3>Authorization</h3>
          <ul>
            <li>You must explicitly authorize access to Gmail and/or Calendar</li>
            <li>You can revoke this authorization at any time through your Google Account settings</li>
            <li>Revoking access will prevent the Service from extracting new tasks</li>
          </ul>

          <h2>5. Acceptable Use</h2>

          <h3>You Agree To</h3>
          <ul>
            <li>Use the Service only for lawful purposes</li>
            <li>Use the Service only for your personal task management</li>
            <li>Comply with all applicable laws and regulations</li>
            <li>Keep your account credentials secure</li>
          </ul>

          <h3>You Agree NOT To</h3>
          <ul>
            <li>Share your account with others</li>
            <li>Use the Service to violate any laws or regulations</li>
            <li>Attempt to gain unauthorized access to the Service or other users' data</li>
            <li>Interfere with or disrupt the Service</li>
            <li>Reverse engineer, decompile, or disassemble the Service</li>
          </ul>

          <h2>6. Your Data</h2>

          <h3>Data You Provide</h3>
          <ul>
            <li>You retain all ownership rights to your data</li>
            <li>You grant us a limited license to access and process your Gmail and Calendar data solely to provide the Service</li>
            <li>You can delete your data at any time</li>
          </ul>

          <h3>Privacy</h3>
          <p>
            Your use of the Service is also governed by our{' '}
            <Link to="/privacy" className="text-blue-600 hover:text-blue-800">
              Privacy Policy
            </Link>.
          </p>

          <h2>7. Google API Services</h2>
          <p>This Service uses Google APIs and is subject to:</p>
          <ul>
            <li>
              <a href="https://developers.google.com/terms/api-services-user-data-policy" target="_blank" rel="noopener noreferrer">
                Google API Services User Data Policy
              </a>
            </li>
            <li>
              <a href="https://policies.google.com/terms" target="_blank" rel="noopener noreferrer">
                Google Terms of Service
              </a>
            </li>
          </ul>

          <h2>8. AI-Generated Content</h2>

          <h3>Task Extraction</h3>
          <ul>
            <li>Tasks are extracted using AI (Google Gemini)</li>
            <li>AI-generated content may not be 100% accurate</li>
            <li>You are responsible for verifying the accuracy of extracted tasks</li>
            <li>We do not guarantee the completeness or correctness of task extraction</li>
          </ul>

          <h3>No Liability for AI Errors</h3>
          <p>We are not liable for:</p>
          <ul>
            <li>Missed tasks or appointments due to AI extraction errors</li>
            <li>Incorrect task information</li>
            <li>Misinterpretation of email or calendar content</li>
          </ul>

          <h2>9. Service Availability</h2>

          <h3>Uptime</h3>
          <ul>
            <li>We strive to keep the Service available 24/7</li>
            <li>We do not guarantee uninterrupted access</li>
            <li>Maintenance windows may occur with or without notice</li>
          </ul>

          <h3>No Warranty</h3>
          <p>
            The Service is provided "AS IS" and "AS AVAILABLE" without warranties of any kind,
            either express or implied.
          </p>

          <h2>10. Limitations of Liability</h2>
          <p>To the maximum extent permitted by law:</p>
          <ul>
            <li>We are not liable for any indirect, incidental, special, or consequential damages</li>
            <li>We are not liable for loss of profits, data, or business opportunities</li>
            <li>Our total liability shall not exceed the amount you paid us in the past 12 months (if any)</li>
          </ul>
          <p>You use the Service at your own risk.</p>

          <h2>11. Account Termination</h2>

          <h3>By You</h3>
          <p>
            You may stop using the Service at any time. To delete your account,
            contact us at support@ai-tasks.app.
          </p>

          <h3>By Us</h3>
          <p>We may suspend or terminate your account if:</p>
          <ul>
            <li>You violate these Terms</li>
            <li>You engage in fraudulent or illegal activity</li>
            <li>We are required to do so by law</li>
            <li>The Service is discontinued</li>
          </ul>

          <h2>12. Intellectual Property</h2>

          <h3>Our Rights</h3>
          <ul>
            <li>The Service, including all content, features, and functionality, is owned by us</li>
            <li>Our trademarks, logos, and service marks are our property</li>
            <li>You may not use our intellectual property without written permission</li>
          </ul>

          <h3>Your Rights</h3>
          <ul>
            <li>You retain all rights to your data</li>
            <li>We do not claim ownership of your emails, calendar events, or extracted tasks</li>
          </ul>

          <h2>13. Changes to Terms</h2>
          <p>
            We may modify these Terms at any time. Changes will be effective immediately upon
            posting for non-material changes, or after 30 days notice for material changes.
            Continued use after changes constitutes acceptance of the modified Terms.
          </p>

          <h2>14. Contact Information</h2>
          <p>For questions about these Terms:</p>
          <p>
            <strong>Email</strong>: support@ai-tasks.app<br />
            <strong>Website</strong>: <a href="https://ai-tasks.app">https://ai-tasks.app</a>
          </p>

          <h2>15. Acknowledgment</h2>
          <p>By using the Service, you acknowledge that:</p>
          <ul>
            <li>You have read and understood these Terms</li>
            <li>You agree to be bound by these Terms</li>
            <li>You have read and understood our Privacy Policy</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default TermsOfService;
