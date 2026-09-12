// Functions to talk to our FastAPI backend

const API_BASE = 'http://localhost:8000';

// Get the auth token from localStorage
function getToken() {
  return localStorage.getItem('access_token');
}

// Make an authenticated request to our backend
async function authFetch(url, options = {}) {
  const token = getToken();
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };
  
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  
  const response = await fetch(`${API_BASE}${url}`, {
    ...options,
    headers,
  });
  
  // If unauthorized, the token is bad - clear it and redirect to login
  if (response.status === 401) {
    localStorage.removeItem('access_token');
    if (window.location.pathname !== '/login') {
      window.location.href = '/login';
    }
  }
  
  return response;
}

// Register a new user
export async function register(email, password, fullName) {
  const response = await fetch(`${API_BASE}/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      email,
      password,
      full_name: fullName || null,
    }),
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Registration failed');
  }
  
  return response.json();
}

// Login and store the JWT token
export async function login(email, password) {
  // OAuth2 expects form data with "username" and "password" fields
  const body = new URLSearchParams();
  body.append('username', email);
  body.append('password', password);
  
  const response = await fetch(`${API_BASE}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: body,
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Login failed');
  }
  
  const data = await response.json();
  localStorage.setItem('access_token', data.access_token);
  return data;
}

// Logout - just clear the token from localStorage
export function logout() {
  localStorage.removeItem('access_token');
}

// Get the current logged-in user
export async function getCurrentUser() {
  const response = await authFetch('/me');
  
  if (!response.ok) {
    throw new Error('Failed to get user info');
  }
  
  return response.json();
}

// Check if user has a valid (non-expired) token
export function isLoggedIn() {
  const token = getToken();
  if (!token || token === 'null' || token === 'undefined' || token === '') {
    return false;
  }
  // If it's a JWT, check expiry - an expired token shouldn't count as logged in
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    if (payload.exp && payload.exp * 1000 < Date.now()) {
      localStorage.removeItem('access_token');
      return false;
    }
  } catch {
    // Not a parseable JWT - fall back to presence check
  }
  return true;
}