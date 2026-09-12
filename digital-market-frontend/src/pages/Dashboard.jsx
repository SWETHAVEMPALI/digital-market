import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { getCurrentUser, logout, isLoggedIn } from '../api';

function Dashboard() {
  const [user, setUser] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    if (!isLoggedIn()) {
      navigate('/login');
      return;
    }

    async function loadUser() {
      try {
        const userData = await getCurrentUser();
        setUser(userData);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    loadUser();
  }, [navigate]);

  function handleLogout(e) {
    e.preventDefault();
    logout();
    navigate('/');
  }

  if (loading) return <div className="card">Loading...</div>;

  return (
    <div className="card">
      <h1>Dashboard</h1>
      {error && <div className="error">{error}</div>}
      
      {user && (
        <>
          <p><strong>Email:</strong> {user.email}</p>
          <p><strong>Name:</strong> {user.full_name || 'Not set'}</p>
          <p>
            <strong>Member since:</strong>{' '}
            {new Date(user.created_at).toLocaleDateString()}
          </p>
          
          <div className="nav" style={{ marginTop: '20px' }}>
            <Link to="/" onClick={handleLogout}>Log out</Link>
          </div>
        </>
      )}
    </div>
  );
}

export default Dashboard;