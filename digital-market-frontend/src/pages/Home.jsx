import { Link } from 'react-router-dom';
import { isLoggedIn } from '../api';

function Home() {
  return (
    <div className="card">
      <h1>Welcome to Digital Market</h1>
      <p>A marketplace for digital products.</p>
      
      <div className="nav" style={{ marginTop: '20px' }}>
        {isLoggedIn() ? (
          <Link to="/dashboard">Go to Dashboard</Link>
        ) : (
          <>
            <Link to="/login">Login</Link>
            <Link to="/signup">Sign up</Link>
          </>
        )}
      </div>
    </div>
  );
}

export default Home;