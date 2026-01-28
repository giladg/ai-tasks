import React from 'react';
import { useNavigate, useLocation, Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

const Header: React.FC = () => {
  const { user, logout, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  if (!isAuthenticated) {
    return null;
  }

  return (
    <header className="bg-white border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 py-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-6">
            <h1 className="text-xl font-bold text-gray-900">AI Task Manager</h1>
            <nav className="flex items-center gap-4">
              <Link
                to="/dashboard"
                className={`text-sm font-medium transition-colors ${
                  location.pathname === '/dashboard'
                    ? 'text-blue-600'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                Dashboard
              </Link>
              {user?.is_admin && (
                <Link
                  to="/admin"
                  className={`text-sm font-medium transition-colors ${
                    location.pathname.startsWith('/admin')
                      ? 'text-blue-600'
                      : 'text-gray-600 hover:text-gray-900'
                  }`}
                >
                  Admin
                </Link>
              )}
            </nav>
          </div>

          <div className="flex items-center gap-4">
            {user && (
              <div className="flex items-center gap-3">
                {user.picture_url && (
                  <img
                    src={user.picture_url}
                    alt={user.name || user.email}
                    className="w-8 h-8 rounded-full"
                  />
                )}
                <div className="text-sm">
                  <div className="font-medium text-gray-900">
                    {user.name || user.email}
                  </div>
                </div>
                <button
                  onClick={handleLogout}
                  className="text-sm text-gray-600 hover:text-gray-900 px-3 py-1 rounded-lg hover:bg-gray-100 transition-colors"
                >
                  Logout
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
