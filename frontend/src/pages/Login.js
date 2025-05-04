// Login.js
import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useUser } from './UserContext'; // Import the context

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();
  const { setUserEmail } = useUser(); // Get the setter from the context

  const handleLogin = async (e) => {
    e.preventDefault();
    setMessage('');

    try {
      const response = await fetch('http://localhost:5000/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (response.ok) {
        setMessage(`Welcome, ${data.user.name}`);
        setUserEmail(email); // Store the email in context
        setTimeout(() => navigate('/home'), 2000);
      } else {
        setMessage(data.message || 'Login failed');
      }
    } catch (err) {
      console.error(err);
      setMessage('Server error');
    }
  };

  return (
    <div style={{ backgroundColor: "#1f2937", color: "white", minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center", padding: "20px" }}>
      <div style={{ width: "100%", maxWidth: "400px" }}>
        <div style={{ display: "flex", justifyContent: "center", marginBottom: "24px" }}>
          <h1 style={{ color: "#a78bfa" }}>NeuralFusion Login</h1>
        </div>
        <div style={{ backgroundColor: "#2d3748", padding: "24px", borderRadius: "8px", boxShadow: "0 0 10px rgba(0,0,0,0.5)" }}>
          {message && (
            <div style={{ marginBottom: "16px", color: message.includes('Welcome') ? "#10b981" : "#f87171" }}>
              {message}
            </div>
          )}
          <form onSubmit={handleLogin} style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
            <input
              type="email"
              placeholder="Enter Email (e.g. john.doe@neuralfusion.com)"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              style={{ padding: "10px", borderRadius: "6px", border: "1px solid #4b5563", backgroundColor: "#374151", color: "white" }}
            />
            <input
              type="password"
              placeholder="Enter Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              style={{ padding: "10px", borderRadius: "6px", border: "1px solid #4b5563", backgroundColor: "#374151", color: "white" }}
            />
            <button
              type="submit"
              style={{ padding: "12px", backgroundColor: "#6366f1", color: "white", border: "none", borderRadius: "6px", fontWeight: "500" }}
            >
              Login
            </button>
          </form>
          <div style={{ marginTop: "16px", textAlign: "center" }}>
            <p style={{ fontSize: "14px", color: "#9ca3af" }}>
              Don’t have an account? <Link to="/signup" style={{ color: "#a78bfa", textDecoration: "none" }}>Sign Up</Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
