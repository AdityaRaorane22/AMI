import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';

const Login = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      const response = await fetch('http://localhost:5000/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();
      
      if (response.status === 200) {
        navigate('/home'); // Redirect to homepage after successful login
      } else {
        setError(data.message);
      }
    } catch (err) {
      console.error(err);
      setError('Server error. Please try again later.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div style={{
      backgroundColor: "#121233",
      color: "white",
      minHeight: "100vh",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      padding: "20px"
    }}>
      <div style={{
        width: "100%",
        maxWidth: "400px"
      }}>
        {/* Logo Header */}
        <div style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          marginBottom: "24px"
        }}>
          <h1 style={{
            color: "#a78bfa",
            margin: 0
          }}>NeuralFusion</h1>
        </div>
        
        {/* Card */}
        <div style={{
          backgroundColor: "rgba(30, 30, 60, 0.5)",
          borderRadius: "8px",
          border: "1px solid rgba(107, 114, 128, 0.3)",
          overflow: "hidden"
        }}>
          {/* Header */}
          <div style={{
            backgroundColor: "rgba(67, 56, 202, 0.1)",
            padding: "16px",
            borderBottom: "1px solid rgba(107, 114, 128, 0.3)",
            textAlign: "center"
          }}>
            <h2 style={{
              fontSize: "24px",
              fontWeight: "bold",
              margin: 0
            }}>Login</h2>
          </div>
          
          {/* Error Message */}
          {error && (
            <div style={{
              backgroundColor: "rgba(239, 68, 68, 0.2)",
              borderLeft: "4px solid #ef4444",
              padding: "12px 16px",
              margin: "16px 16px 0 16px",
              borderRadius: "0 4px 4px 0"
            }}>
              <p style={{
                color: "#fecaca",
                margin: 0,
                fontSize: "14px"
              }}>{error}</p>
            </div>
          )}
          
          {/* Form */}
          <form onSubmit={handleSubmit} style={{
            padding: "24px",
            display: "flex",
            flexDirection: "column",
            gap: "20px"
          }}>
            <div>
              <label htmlFor="email" style={{
                display: "block",
                fontSize: "14px",
                marginBottom: "8px",
                color: "#d1d5db"
              }}>Email</label>
              <input
                id="email"
                name="email"
                type="email"
                required
                value={formData.email}
                onChange={handleChange}
                style={{
                  width: "100%",
                  padding: "10px 12px",
                  backgroundColor: "rgba(17, 24, 39, 0.5)",
                  border: "1px solid rgba(107, 114, 128, 0.3)",
                  borderRadius: "6px",
                  color: "white",
                  fontSize: "16px"
                }}
                placeholder="your@email.com"
              />
            </div>
            
            <div>
              <label htmlFor="password" style={{
                display: "block",
                fontSize: "14px",
                marginBottom: "8px",
                color: "#d1d5db"
              }}>Password</label>
              <input
                id="password"
                name="password"
                type="password"
                required
                value={formData.password}
                onChange={handleChange}
                style={{
                  width: "100%",
                  padding: "10px 12px",
                  backgroundColor: "rgba(17, 24, 39, 0.5)",
                  border: "1px solid rgba(107, 114, 128, 0.3)",
                  borderRadius: "6px",
                  color: "white",
                  fontSize: "16px"
                }}
                placeholder="••••••••"
              />
            </div>
            
            <div style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center"
            }}>
              <div style={{
                display: "flex",
                alignItems: "center"
              }}>
                <input
                  id="remember-me"
                  name="remember-me"
                  type="checkbox"
                  style={{
                    marginRight: "8px"
                  }}
                />
                <label htmlFor="remember-me" style={{
                  fontSize: "14px",
                  color: "#d1d5db"
                }}>
                  Remember me
                </label>
              </div>
              
              <a href="#" style={{
                fontSize: "14px",
                color: "#a78bfa",
                textDecoration: "none"
              }}>
                Forgot password?
              </a>
            </div>
            
            <button
              type="submit"
              disabled={isSubmitting}
              style={{
                width: "100%",
                padding: "12px",
                backgroundColor: "#6366f1",
                color: "white",
                border: "none",
                borderRadius: "6px",
                fontSize: "16px",
                fontWeight: "500",
                cursor: isSubmitting ? "not-allowed" : "pointer",
                opacity: isSubmitting ? 0.7 : 1
              }}
            >
              {isSubmitting ? 'Logging in...' : 'Login'}
            </button>
          </form>
          
          {/* Footer */}
          <div style={{
            padding: "16px",
            backgroundColor: "rgba(17, 24, 39, 0.3)",
            borderTop: "1px solid rgba(107, 114, 128, 0.3)",
            textAlign: "center"
          }}>
            <p style={{
              fontSize: "14px",
              color: "#9ca3af",
              margin: 0
            }}>
              Don't have an account?{' '}
              <Link to="/signup" style={{
                color: "#a78bfa",
                textDecoration: "none",
                fontWeight: "500"
              }}>
                Sign Up
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;