import React, { useState, useEffect } from 'react';
import { Cpu, Brain, Zap, Database } from 'lucide-react';
import { motion } from 'framer-motion';

const fadeInUp = {
  hidden: { opacity: 0, y: 20 },
  visible: (i = 1) => ({
    opacity: 1,
    y: 0,
    transition: { delay: i * 0.2, duration: 0.6 }
  })
};

const slideInFromLeft = {
  hidden: { opacity: 0, x: -100 },
  visible: (i = 1) => ({
    opacity: 1,
    x: 0,
    transition: { delay: i * 0.2, duration: 0.6 }
  })
};

const slideInFromRight = {
  hidden: { opacity: 0, x: 100 },
  visible: (i = 1) => ({
    opacity: 1,
    x: 0,
    transition: { delay: i * 0.2, duration: 0.6 }
  })
};

const fadeInFromBottom = {
  hidden: { opacity: 0, y: 100 },
  visible: (i = 1) => ({
    opacity: 1,
    y: 0,
    transition: { delay: i * 0.2, duration: 0.6 }
  })
};

const Landing = () => {
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    setIsLoaded(true);
  }, []);

  const features = [
    {
      icon: <Brain size={24} />,
      title: "Neural Networks",
      description: "Advanced deep learning algorithms that mimic human brain functionality"
    },
    {
      icon: <Cpu size={24} />,
      title: "Optimized Processing",
      description: "Efficient computation designed for complex AI tasks and real-time inference"
    },
    {
      icon: <Database size={24} />,
      title: "Data Intelligence",
      description: "Transform raw data into actionable insights with our smart analytics"
    },
    {
      icon: <Zap size={24} />,
      title: "Lightning Fast",
      description: "Accelerated model training and deployment for rapid implementation"
    }
  ];

  return (
    <div style={{ backgroundColor: "#121233", color: "white", minHeight: "100vh", padding: "20px" }}>
      {/* Header */}
      <motion.header
        initial="hidden"
        animate="visible"
        variants={fadeInUp}
        style={{
          display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "40px"
        }}
      >
        <div style={{ display: "flex", alignItems: "center" }}>
          <div style={{
            width: "40px",
            height: "40px",
            backgroundColor: "#6366f1",
            borderRadius: "8px",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            marginRight: "15px"
          }}>
            <Cpu color="white" size={24} />
          </div>
          <h1 style={{ margin: 0, color: "#a78bfa" }}>NeuralFusion</h1>
        </div>

        <nav>
          <ul style={{ display: "flex", listStyle: "none", gap: "20px", margin: 0, padding: 0 }}>
            <li><a href="#features" style={{ color: "white", textDecoration: "none" }}>Features</a></li>
            <li><a href="#technology" style={{ color: "white", textDecoration: "none" }}>Technology</a></li>
            <li><a href="#about" style={{ color: "white", textDecoration: "none" }}>About</a></li>
          </ul>
        </nav>

        <button style={{
          backgroundColor: "#6366f1",
          border: "none",
          color: "white",
          padding: "10px 20px",
          borderRadius: "8px",
          cursor: "pointer"
        }}>
          Get Started
        </button>
      </motion.header>

      {/* Hero Section */}
      <motion.section
        initial="hidden"
        animate="visible"
        variants={slideInFromLeft}
        style={{
          margin: "0 auto 60px auto",
          maxWidth: "1200px",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          textAlign: "center"
        }}
      >
        <motion.h2
          variants={fadeInUp}
          style={{
            fontSize: "48px",
            background: "linear-gradient(to right, #a78bfa, #818cf8)",
            WebkitBackgroundClip: "text",
            WebkitTextFillColor: "transparent",
            marginBottom: "20px"
          }}
        >
          Next Generation AI Solutions
        </motion.h2>
        <motion.p
          variants={fadeInUp}
          style={{
            fontSize: "18px",
            color: "#d1d5db",
            maxWidth: "700px",
            marginBottom: "30px"
          }}
        >
          Harnessing the power of advanced machine learning to transform how you interact with technology and data.
        </motion.p>
        <motion.button
          variants={fadeInUp}
          style={{
            backgroundColor: "#6366f1",
            border: "none",
            color: "white",
            padding: "12px 24px",
            borderRadius: "8px",
            cursor: "pointer",
            fontSize: "16px",
            fontWeight: "bold"
          }}
        >
          Explore Solutions
        </motion.button>
      </motion.section>

      {/* Features Section */}
      <motion.section
        id="features"
        initial="hidden"
        animate="visible"
        variants={fadeInUp}
        style={{
          margin: "0 auto 60px auto",
          maxWidth: "1200px",
          padding: "40px 20px",
          backgroundColor: "rgba(0,0,0,0.3)",
          borderRadius: "16px"
        }}
      >
        <h2 style={{
          textAlign: "center",
          fontSize: "36px",
          marginBottom: "40px",
          color: "#a78bfa"
        }}>
          Cutting-Edge AI Features
        </h2>

        <div style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(250px, 1fr))",
          gap: "20px"
        }}>
          {features.map((feature, index) => (
            <motion.div
              key={index}
              custom={index}
              variants={fadeInUp}
              initial="hidden"
              animate="visible"
              style={{
                backgroundColor: "rgba(30,30,60,0.5)",
                padding: "24px",
                borderRadius: "12px",
                border: "1px solid rgba(255,255,255,0.1)"
              }}
            >
              <div style={{ marginBottom: "16px", color: "#a78bfa" }}>
                {feature.icon}
              </div>
              <h3 style={{ marginBottom: "8px", fontSize: "20px" }}>{feature.title}</h3>
              <p style={{ color: "#9ca3af" }}>{feature.description}</p>
            </motion.div>
          ))}
        </div>
      </motion.section>

      {/* Technology Section */}
      <motion.section
        id="technology"
        initial="hidden"
        animate="visible"
        variants={slideInFromRight}
        style={{
          margin: "0 auto 60px auto",
          maxWidth: "1200px",
          padding: "40px 20px"
        }}
      >
        <h2 style={{
          textAlign: "center",
          fontSize: "36px",
          marginBottom: "20px",
          color: "#a78bfa"
        }}>
          Our Technology
        </h2>
        <div style={{
          backgroundColor: "rgba(30,30,60,0.5)",
          padding: "24px",
          borderRadius: "12px",
          border: "1px solid rgba(255,255,255,0.1)"
        }}>
          <p style={{ textAlign: "center", color: "#d1d5db" }}>
            Advanced machine learning algorithms and neural networks that power our AI solutions.
          </p>
        </div>
      </motion.section>

      {/* About Section */}
      <motion.section
        id="about"
        initial="hidden"
        animate="visible"
        variants={fadeInFromBottom}
        style={{
          margin: "0 auto 60px auto",
          maxWidth: "1200px",
          padding: "40px 20px"
        }}
      >
        <h2 style={{
          textAlign: "center",
          fontSize: "36px",
          marginBottom: "20px",
          color: "#a78bfa"
        }}>
          About Us
        </h2>
        <div style={{
          backgroundColor: "rgba(30,30,60,0.5)",
          padding: "24px",
          borderRadius: "12px",
          border: "1px solid rgba(255,255,255,0.1)"
        }}>
          <p style={{ textAlign: "center", color: "#d1d5db" }}>
            We are a team of passionate AI researchers and engineers dedicated to pushing the boundaries of what's possible.
          </p>
        </div>
      </motion.section>

      {/* CTA Section */}
      <motion.section
        initial="hidden"
        animate="visible"
        variants={fadeInUp}
        style={{
          margin: "0 auto 60px auto",
          maxWidth: "1200px",
          padding: "40px 20px",
          backgroundColor: "rgba(60,60,120,0.3)",
          borderRadius: "16px",
          textAlign: "center"
        }}
      >
        <h2 style={{ fontSize: "32px", marginBottom: "20px" }}>Ready to Transform Your AI Capabilities?</h2>
        <p style={{
          color: "#d1d5db",
          marginBottom: "30px",
          maxWidth: "800px",
          margin: "0 auto 30px auto"
        }}>
          Join the future of intelligent technology. Our platform offers seamless integration,
          powerful analytics, and cutting-edge machine learning tools.
        </p>
        <button style={{
          backgroundColor: "#6366f1",
          border: "none",
          color: "white",
          padding: "12px 24px",
          borderRadius: "8px",
          cursor: "pointer",
          fontSize: "16px",
          fontWeight: "bold"
        }}>
          Start Your Journey
        </button>
      </motion.section>
    </div>
  );
};

export default Landing;
