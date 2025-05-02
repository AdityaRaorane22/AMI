import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';

const Signup = () => {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    dob: '',
    gender: '',
    mobile: '',
    email: '',
    password: '',
    confirmPassword: '',
  });

  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    try {
      const response = await fetch('http://localhost:5000/signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (response.status === 201) {
        navigate('/login');
      } else {
        setError(data.message);
      }
    } catch (err) {
      console.error(err);
      setError('Server error');
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
      <div style={{ width: "100%", maxWidth: "500px" }}>
        <div style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          marginBottom: "24px"
        }}>
          <h1 style={{ color: "#a78bfa", margin: 0 }}>NeuralFusion</h1>
        </div>

        <div style={{
          backgroundColor: "rgba(30, 30, 60, 0.5)",
          borderRadius: "8px",
          border: "1px solid rgba(107, 114, 128, 0.3)",
          overflow: "hidden"
        }}>
          <div style={{
            backgroundColor: "rgba(67, 56, 202, 0.1)",
            padding: "16px",
            textAlign: "center",
            borderBottom: "1px solid rgba(107, 114, 128, 0.3)"
          }}>
            <h2 style={{
              fontSize: "24px",
              fontWeight: "bold",
              margin: 0
            }}>Signup</h2>
          </div>

          {error && (
            <div style={{
              backgroundColor: "rgba(239, 68, 68, 0.2)",
              borderLeft: "4px solid #ef4444",
              padding: "12px 16px",
              margin: "16px 16px 0 16px",
              borderRadius: "0 4px 4px 0"
            }}>
              <p style={{ color: "#fecaca", margin: 0, fontSize: "14px" }}>{error}</p>
            </div>
          )}

          <form onSubmit={handleSubmit} style={{
            padding: "24px",
            display: "flex",
            flexDirection: "column",
            gap: "16px"
          }}>
            {[
              { name: "firstName", type: "text", placeholder: "First Name" },
              { name: "lastName", type: "text", placeholder: "Last Name" },
              { name: "dob", type: "date", placeholder: "Date of Birth" },
              { name: "gender", type: "text", placeholder: "Gender" },
              { name: "mobile", type: "text", placeholder: "Mobile Number" },
              { name: "email", type: "email", placeholder: "Email" },
              { name: "password", type: "password", placeholder: "Password" },
              { name: "confirmPassword", type: "password", placeholder: "Confirm Password" },
            ].map(({ name, type, placeholder }) => (
              <input
                key={name}
                name={name}
                type={type}
                value={formData[name]}
                onChange={handleChange}
                placeholder={placeholder}
                required
                style={{
                  width: "100%",
                  padding: "10px 12px",
                  backgroundColor: "rgba(17, 24, 39, 0.5)",
                  border: "1px solid rgba(107, 114, 128, 0.3)",
                  borderRadius: "6px",
                  color: "white",
                  fontSize: "16px"
                }}
              />
            ))}

            <button
              type="submit"
              style={{
                width: "100%",
                padding: "12px",
                backgroundColor: "#6366f1",
                color: "white",
                border: "none",
                borderRadius: "6px",
                fontSize: "16px",
                fontWeight: "500",
                cursor: "pointer"
              }}
            >
              Sign Up
            </button>
          </form>

          <div style={{
            padding: "16px",
            backgroundColor: "rgba(17, 24, 39, 0.3)",
            borderTop: "1px solid rgba(107, 114, 128, 0.3)",
            textAlign: "center"
          }}>
            <p style={{ fontSize: "14px", color: "#9ca3af", margin: 0 }}>
              Already have an account?{' '}
              <Link to="/login" style={{
                color: "#a78bfa",
                textDecoration: "none"
              }}>
                Login
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Signup;
