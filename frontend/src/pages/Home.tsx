import React from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Home: React.FC = () => {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();

  React.useEffect(() => {
    if (isAuthenticated) {
      navigate('/dashboard');
    }
  }, [isAuthenticated, navigate]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="max-w-7xl mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <div className="flex justify-center mb-8">
            <img src="/logo.svg" alt="AI Task Manager Logo" className="w-24 h-24" />
          </div>
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            AI-Powered Task Management
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Automatically extract and manage tasks from your Gmail and Google Calendar
          </p>
          <button
            onClick={() => navigate('/login')}
            className="bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors shadow-lg"
          >
            Get Started
          </button>
        </div>

        <div className="grid md:grid-cols-3 gap-8 mb-16">
          <div className="bg-white rounded-xl p-6 shadow-lg">
            <div className="text-blue-600 mb-4">
              <svg
                className="w-12 h-12"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              Automatic Extraction
            </h3>
            <p className="text-gray-600">
              AI analyzes your emails and calendar to find actionable tasks automatically
            </p>
          </div>

          <div className="bg-white rounded-xl p-6 shadow-lg">
            <div className="text-blue-600 mb-4">
              <svg
                className="w-12 h-12"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4"
                />
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Smart Prioritization</h3>
            <p className="text-gray-600">
              Tasks are automatically prioritized based on urgency and importance
            </p>
          </div>

          <div className="bg-white rounded-xl p-6 shadow-lg">
            <div className="text-blue-600 mb-4">
              <svg
                className="w-12 h-12"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
                />
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Learns From You</h3>
            <p className="text-gray-600">
              The system improves over time based on your edits and preferences
            </p>
          </div>
        </div>

        {/* Footer */}
        <footer className="text-center text-gray-600 mt-16">
          <div className="flex justify-center gap-6 mb-4">
            <Link to="/privacy" className="hover:text-blue-600 transition-colors">
              Privacy Policy
            </Link>
            <Link to="/terms" className="hover:text-blue-600 transition-colors">
              Terms of Service
            </Link>
          </div>
          <p className="text-sm">
            © 2026 AI Task Manager. All rights reserved.
          </p>
        </footer>
      </div>
    </div>
  );
};

export default Home;
