import React, { useState } from 'react';
import { useUser } from './UserContext';
import ReactMarkdown from 'react-markdown';
import { Shield, Send, PieChart, Lock, Info, Bell, CheckCircle, X } from 'lucide-react';

const Home = () => {
  const { userEmail } = useUser();
  const [showChat, setShowChat] = useState(false);
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([]);
  const [activeTab, setActiveTab] = useState('dashboard');
  const [notification, setNotification] = useState(null);

  // Cybersecurity news and tips content
  const securityTips = [
    {
      title: "Enable Multi-Factor Authentication",
      description: "Add an extra layer of security to your accounts by enabling MFA wherever possible."
    },
    {
      title: "Keep Software Updated",
      description: "Regular updates patch security vulnerabilities in your operating system and applications."
    },
    {
      title: "Use Strong, Unique Passwords",
      description: "Create complex passwords and avoid reusing them across different accounts."
    },
    {
      title: "Be Wary of Phishing Attempts",
      description: "Verify the sender before clicking links or downloading attachments in emails."
    }
  ];

  const recentThreats = [
    {
      title: "Ransomware Campaign Targeting Healthcare",
      level: "Critical",
      date: "May 2, 2025"
    },
    {
      title: "Zero-day Vulnerability in Popular Browser",
      level: "High",
      date: "April 29, 2025"
    },
    {
      title: "New Phishing Technique Using AI Voice Cloning",
      level: "Medium",
      date: "April 25, 2025"
    }
  ];

  const handleSend = async () => {
    if (!query.trim()) return;

    const userMessage = { sender: 'user', text: query };
    setMessages(prev => [...prev, userMessage]);

    try {
      const response = await fetch('http://localhost:7000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
      });

      const data = await response.json();
      const aiMessage = { sender: 'bot', text: data.response };
      setMessages(prev => [...prev, aiMessage]);
    } catch (err) {
      setMessages(prev => [...prev, { sender: 'bot', text: 'Error contacting server.' }]);
    }

    setQuery('');
  };

  const handlePrediction = () => {
    window.location.href = 'http://localhost:8501';
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSend();
    }
  };

  const showNotification = (message, type = 'success') => {
    setNotification({ message, type });
    setTimeout(() => setNotification(null), 3000);
  };

  const switchTab = (tab) => {
    setActiveTab(tab);
    if (tab === 'chat') {
      setShowChat(true);
    } else {
      setShowChat(false);
    }
  };

  return (
    <div style={{
      fontFamily: "'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif",
      color: '#333',
      maxWidth: '1200px',
      margin: '0 auto',
      padding: '20px',
      backgroundColor: '#f8f9fa',
      minHeight: '100vh',
      position: 'relative'
    }}>
      {/* Header */}
      <header style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '30px',
        padding: '15px 20px',
        backgroundColor: '#2c3e50',
        borderRadius: '10px',
        color: 'white',
        boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)'
      }}>
        <div style={{ display: 'flex', alignItems: 'center' }}>
          <Shield size={28} style={{ marginRight: '12px' }} />
          <h1 style={{ margin: 0, fontSize: '24px' }}>SafeShield</h1>
        </div>
        <div style={{ display: 'flex', alignItems: 'center' }}>
          <span style={{ marginRight: '20px' }}>Welcome, {userEmail}</span>
          <div style={{
            width: '40px',
            height: '40px',
            borderRadius: '50%',
            backgroundColor: '#3498db',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontWeight: 'bold'
          }}>
            {userEmail.charAt(0).toUpperCase()}
          </div>
        </div>
      </header>

      {/* Notification */}
      {notification && (
        <div style={{
          position: 'fixed',
          top: '20px',
          right: '20px',
          padding: '12px 24px',
          borderRadius: '8px',
          backgroundColor: notification.type === 'success' ? '#2ecc71' : '#e74c3c',
          color: 'white',
          zIndex: 1000,
          display: 'flex',
          alignItems: 'center',
          boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)'
        }}>
          {notification.type === 'success' ? <CheckCircle size={18} style={{ marginRight: '8px' }} /> : <X size={18} style={{ marginRight: '8px' }} />}
          {notification.message}
        </div>
      )}

      {/* Navigation Tabs */}
      <div style={{
        display: 'flex',
        marginBottom: '30px',
        backgroundColor: 'white',
        borderRadius: '8px',
        overflow: 'hidden',
        boxShadow: '0 2px 4px rgba(0, 0, 0, 0.05)'
      }}>
        <div 
          onClick={() => switchTab('dashboard')}
          style={{
            padding: '15px 25px',
            cursor: 'pointer',
            backgroundColor: activeTab === 'dashboard' ? '#3498db' : 'transparent',
            color: activeTab === 'dashboard' ? 'white' : '#555',
            fontWeight: 'bold',
            display: 'flex',
            alignItems: 'center',
            transition: 'all 0.3s ease'
          }}
        >
          <PieChart size={18} style={{ marginRight: '8px' }} />
          Dashboard
        </div>
        <div 
          onClick={() => switchTab('chat')}
          style={{
            padding: '15px 25px',
            cursor: 'pointer',
            backgroundColor: activeTab === 'chat' ? '#3498db' : 'transparent',
            color: activeTab === 'chat' ? 'white' : '#555',
            fontWeight: 'bold',
            display: 'flex',
            alignItems: 'center',
            transition: 'all 0.3s ease'
          }}
        >
          <Send size={18} style={{ marginRight: '8px' }} />
          Chatbot
        </div>
        <div 
          onClick={() => {
            switchTab('prediction');
            handlePrediction();
          }}
          style={{
            padding: '15px 25px',
            cursor: 'pointer',
            backgroundColor: activeTab === 'prediction' ? '#3498db' : 'transparent',
            color: activeTab === 'prediction' ? 'white' : '#555',
            fontWeight: 'bold',
            display: 'flex',
            alignItems: 'center',
            transition: 'all 0.3s ease'
          }}
        >
          <Lock size={18} style={{ marginRight: '8px' }} />
          Threat Prediction
        </div>
      </div>

      {/* Main Content Area */}
      <div style={{
        display: 'flex',
        gap: '30px'
      }}>
        {/* Left Column - Dashboard Content */}
        {activeTab === 'dashboard' && (
          <div style={{
            flex: '7',
            display: 'flex',
            flexDirection: 'column',
            gap: '30px'
          }}>
            {/* Security Status Card */}
            <div style={{
              backgroundColor: 'white',
              borderRadius: '10px',
              padding: '25px',
              boxShadow: '0 2px 10px rgba(0, 0, 0, 0.05)'
            }}>
              <h2 style={{ margin: '0 0 20px 0', color: '#2c3e50', display: 'flex', alignItems: 'center' }}>
                <Shield size={24} style={{ marginRight: '10px' }} />
                Security Status
              </h2>
              <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                textAlign: 'center'
              }}>
                <div style={{ flex: 1 }}>
                  <div style={{
                    width: '100px',
                    height: '100px',
                    borderRadius: '50%',
                    backgroundColor: '#2ecc71',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    margin: '0 auto 15px',
                    color: 'white',
                    fontSize: '24px',
                    fontWeight: 'bold'
                  }}>
                    92%
                  </div>
                  <p style={{ margin: '0', fontWeight: 'bold' }}>Security Score</p>
                </div>
                <div style={{ flex: 1 }}>
                  <div style={{
                    width: '100px',
                    height: '100px',
                    borderRadius: '50%',
                    backgroundColor: '#3498db',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    margin: '0 auto 15px',
                    color: 'white',
                    fontSize: '24px',
                    fontWeight: 'bold'
                  }}>
                    0
                  </div>
                  <p style={{ margin: '0', fontWeight: 'bold' }}>Active Threats</p>
                </div>
                <div style={{ flex: 1 }}>
                  <div style={{
                    width: '100px',
                    height: '100px',
                    borderRadius: '50%',
                    backgroundColor: '#f39c12',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    margin: '0 auto 15px',
                    color: 'white',
                    fontSize: '24px',
                    fontWeight: 'bold'
                  }}>
                    2
                  </div>
                  <p style={{ margin: '0', fontWeight: 'bold' }}>Warnings</p>
                </div>
              </div>
            </div>

            {/* Recent Threats */}
            <div style={{
              backgroundColor: 'white',
              borderRadius: '10px',
              padding: '25px',
              boxShadow: '0 2px 10px rgba(0, 0, 0, 0.05)'
            }}>
              <h2 style={{ margin: '0 0 20px 0', color: '#2c3e50', display: 'flex', alignItems: 'center' }}>
                <Bell size={24} style={{ marginRight: '10px' }} />
                Recent Threats
              </h2>
              <div>
                {recentThreats.map((threat, index) => (
                  <div key={index} style={{
                    padding: '15px',
                    borderLeft: `4px solid ${
                      threat.level === 'Critical' ? '#e74c3c' : 
                      threat.level === 'High' ? '#f39c12' : 
                      '#3498db'
                    }`,
                    backgroundColor: '#f8f9fa',
                    marginBottom: '10px',
                    borderRadius: '4px'
                  }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                      <h3 style={{ margin: '0', fontSize: '16px' }}>{threat.title}</h3>
                      <span style={{
                        padding: '2px 8px',
                        borderRadius: '12px',
                        fontSize: '12px',
                        backgroundColor: 
                          threat.level === 'Critical' ? '#e74c3c' : 
                          threat.level === 'High' ? '#f39c12' : 
                          '#3498db',
                        color: 'white'
                      }}>
                        {threat.level}
                      </span>
                    </div>
                    <p style={{ margin: '5px 0 0 0', color: '#7f8c8d', fontSize: '14px' }}>{threat.date}</p>
                  </div>
                ))}
              </div>
              <button style={{
                backgroundColor: 'transparent',
                border: '1px solid #3498db',
                color: '#3498db',
                padding: '8px 15px',
                borderRadius: '5px',
                cursor: 'pointer',
                fontWeight: 'bold',
                display: 'block',
                margin: '15px 0 0 auto',
                transition: 'all 0.3s ease'
              }}
              onClick={() => showNotification('Viewing all threats is not available in this demo', 'error')}
              >
                View All Threats
              </button>
            </div>
          </div>
        )}

        {/* Right Column - Always visible */}
        <div style={{
          flex: '3',
          display: 'flex',
          flexDirection: 'column',
          gap: '30px'
        }}>
          {/* Security Tips */}
          <div style={{
            backgroundColor: 'white',
            borderRadius: '10px',
            padding: '25px',
            boxShadow: '0 2px 10px rgba(0, 0, 0, 0.05)'
          }}>
            <h2 style={{ margin: '0 0 20px 0', color: '#2c3e50', display: 'flex', alignItems: 'center' }}>
              <Info size={24} style={{ marginRight: '10px' }} />
              Security Tips
            </h2>
            {securityTips.map((tip, index) => (
              <div key={index} style={{ marginBottom: '15px' }}>
                <h3 style={{ margin: '0 0 5px 0', fontSize: '16px' }}>{tip.title}</h3>
                <p style={{ margin: '0', color: '#7f8c8d', fontSize: '14px' }}>{tip.description}</p>
              </div>
            ))}
          </div>

          {/* Chat Window */}
          {showChat && (
            <div style={{
              backgroundColor: 'white',
              borderRadius: '10px',
              overflow: 'hidden',
              boxShadow: '0 2px 10px rgba(0, 0, 0, 0.05)',
              flex: '1',
              display: 'flex',
              flexDirection: 'column',
              maxHeight: activeTab === 'chat' ? '600px' : '400px'
            }}>
              <div style={{
                backgroundColor: '#2c3e50',
                color: 'white',
                padding: '15px',
                fontWeight: 'bold',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between'
              }}>
                <div style={{ display: 'flex', alignItems: 'center' }}>
                  <Shield size={18} style={{ marginRight: '8px' }} />
                  Cybersecurity Assistant
                </div>
                {activeTab !== 'chat' && (
                  <span 
                    style={{ cursor: 'pointer' }}
                    onClick={() => switchTab('chat')}
                  >
                    Expand
                  </span>
                )}
              </div>
              <div style={{
                padding: '15px',
                maxHeight: activeTab === 'chat' ? '450px' : '250px',
                overflowY: 'auto',
                flex: '1'
              }}>
                <p style={{
                  color: '#7f8c8d',
                  fontStyle: 'italic',
                  marginBottom: '20px'
                }}>
                  Ask me anything about cybersecurity! I'm here to assist you.
                </p>
                {messages.map((msg, index) => (
                  <div key={index} style={{
                    padding: '10px 15px',
                    borderRadius: '10px',
                    maxWidth: '80%',
                    marginBottom: '10px',
                    backgroundColor: msg.sender === 'user' ? '#3498db' : '#f2f2f2',
                    color: msg.sender === 'user' ? 'white' : '#333',
                    alignSelf: msg.sender === 'user' ? 'flex-end' : 'flex-start',
                    marginLeft: msg.sender === 'user' ? 'auto' : '0'
                  }}>
                    <strong>{msg.sender === 'user' ? 'You' : 'Bot'}:</strong>{' '}
                    {msg.sender === 'bot' ? <ReactMarkdown>{msg.text}</ReactMarkdown> : msg.text}
                  </div>
                ))}
              </div>
              <div style={{
                padding: '15px',
                display: 'flex',
                borderTop: '1px solid #e1e1e1'
              }}>
                <input
                  type="text"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Ask a cybersecurity question..."
                  style={{
                    flex: '1',
                    padding: '12px 15px',
                    borderRadius: '5px',
                    border: '1px solid #e1e1e1',
                    outline: 'none',
                    marginRight: '10px'
                  }}
                />
                <button 
                  onClick={handleSend}
                  style={{
                    backgroundColor: '#3498db',
                    color: 'white',
                    border: 'none',
                    borderRadius: '5px',
                    padding: '0 20px',
                    fontWeight: 'bold',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center'
                  }}
                >
                  <Send size={18} />
                </button>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Footer */}
      <footer style={{
        marginTop: '40px',
        padding: '20px 0',
        borderTop: '1px solid #e1e1e1',
        textAlign: 'center',
        color: '#7f8c8d',
        fontSize: '14px'
      }}>
        <p>&copy; 2025 SafeShield Platform. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default Home;