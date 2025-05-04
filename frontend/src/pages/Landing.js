import React, { useState, useEffect } from 'react';
import { Shield, Lock, Eye, AlertCircle, Database, UserCheck } from 'lucide-react';

const Landing = () => {
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    setIsLoaded(true);
  }, []);

  const features = [
    {
      icon: <Shield size={24} />,
      title: "Advanced Protection",
      description: "Enterprise-grade security that safeguards your sensitive data from threats"
    },
    {
      icon: <Lock size={24} />,
      title: "Robust Encryption",
      description: "Military-grade encryption protocols to keep your information secure and private"
    },
    {
      icon: <Eye size={24} />,
      title: "Threat Monitoring",
      description: "24/7 vigilant monitoring to detect and prevent security breaches in real-time"
    },
    {
      icon: <AlertCircle size={24} />,
      title: "Incident Response",
      description: "Rapid alert system and expert team to address security incidents immediately"
    },
    {
      icon: <Database size={24} />,
      title: "Secure Storage",
      description: "Protected data repositories with multiple layers of access control"
    },
    {
      icon: <UserCheck size={24} />,
      title: "Identity Protection",
      description: "Advanced authentication systems to verify and protect user identities"
    }
  ];

  return (
    <div className="bg-slate-900 text-white min-h-screen p-5">
      {/* Header */}
      <header className="flex justify-between items-center mb-10">
        <div className="flex items-center">
          <div className="w-10 h-10 bg-blue-600 rounded-md flex items-center justify-center mr-4">
            <Shield color="white" size={24} />
          </div>
          <h1 className="m-0 text-blue-400 text-2xl font-bold">SafeShield</h1>
        </div>

        <nav>
          <ul className="flex list-none gap-5 m-0 p-0">
            <li><a href="#features" className="text-white no-underline hover:text-blue-400">Features</a></li>
            <li><a href="#technology" className="text-white no-underline hover:text-blue-400">Technology</a></li>
            <li><a href="#about" className="text-white no-underline hover:text-blue-400">About</a></li>
          </ul>
        </nav>

        <button className="bg-blue-600 border-none text-white py-2 px-5 rounded-md cursor-pointer hover:bg-blue-700">
          Get Protected
        </button>
      </header>

      {/* Hero Section */}
      <section className="mx-auto mb-16 max-w-6xl flex flex-col items-center text-center">
        <h2 className="text-5xl mb-5 font-bold bg-gradient-to-r from-blue-400 to-blue-600 bg-clip-text text-transparent">
          Enterprise Security Solutions
        </h2>
        <p className="text-lg text-gray-300 max-w-2xl mb-8">
          Comprehensive cybersecurity platform designed to protect your business from evolving digital threats and vulnerabilities.
        </p>
        <div className="flex gap-4">
          <button className="bg-blue-600 border-none text-white py-3 px-6 rounded-md cursor-pointer text-base font-bold hover:bg-blue-700">
            Start Free Trial
          </button>
          <button className="bg-transparent border border-blue-600 text-white py-3 px-6 rounded-md cursor-pointer text-base font-bold hover:bg-blue-900">
            See Demo
          </button>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="mx-auto mb-16 max-w-6xl p-10 bg-slate-800 bg-opacity-50 rounded-xl">
        <h2 className="text-center text-3xl mb-10 text-blue-400 font-bold">
          Complete Security Features
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => (
            <div
              key={index}
              className="bg-slate-800 p-6 rounded-xl border border-slate-700 hover:border-blue-500 transition-all duration-300"
            >
              <div className="mb-4 text-blue-400">
                {feature.icon}
              </div>
              <h3 className="mb-2 text-xl font-semibold">{feature.title}</h3>
              <p className="text-gray-400">{feature.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Technology Section */}
      <section id="technology" className="mx-auto mb-16 max-w-6xl p-10">
        <h2 className="text-center text-3xl mb-6 text-blue-400 font-bold">
          Our Security Technology
        </h2>
        <div className="bg-slate-800 p-8 rounded-xl border border-slate-700">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div>
              <h3 className="text-xl mb-4 font-semibold">Cutting-Edge Protection</h3>
              <ul className="space-y-2 text-gray-300">
                <li className="flex items-center">
                  <Shield size={16} className="mr-2 text-blue-400" />
                  Multi-layered firewall infrastructure
                </li>
                <li className="flex items-center">
                  <Shield size={16} className="mr-2 text-blue-400" />
                  Advanced intrusion detection systems
                </li>
                <li className="flex items-center">
                  <Shield size={16} className="mr-2 text-blue-400" />
                  Behavioral analytics and anomaly detection
                </li>
                <li className="flex items-center">
                  <Shield size={16} className="mr-2 text-blue-400" />
                  End-to-end data encryption
                </li>
              </ul>
            </div>
            <div>
              <h3 className="text-xl mb-4 font-semibold">Industry Compliance</h3>
              <ul className="space-y-2 text-gray-300">
                <li className="flex items-center">
                  <Lock size={16} className="mr-2 text-blue-400" />
                  GDPR compliant data handling
                </li>
                <li className="flex items-center">
                  <Lock size={16} className="mr-2 text-blue-400" />
                  HIPAA certified security protocols
                </li>
                <li className="flex items-center">
                  <Lock size={16} className="mr-2 text-blue-400" />
                  ISO 27001 certification
                </li>
                <li className="flex items-center">
                  <Lock size={16} className="mr-2 text-blue-400" />
                  SOC 2 Type II audited
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* About Section */}
      <section id="about" className="mx-auto mb-16 max-w-6xl p-10 bg-slate-800 bg-opacity-30 rounded-xl">
        <h2 className="text-center text-3xl mb-5 text-blue-400 font-bold">
          About Safe Shield
        </h2>
        <div className="text-center text-gray-300 max-w-3xl mx-auto">
          <p className="mb-6">
            Founded by cybersecurity experts with over 50 years of combined experience in the industry, 
            Safe Shield was created with a simple mission: to provide enterprise-grade security solutions 
            that are accessible to businesses of all sizes.
          </p>
          <p>
            Our team of certified security professionals works tirelessly to stay ahead of emerging threats 
            and develop innovative solutions that keep your business protected in an ever-evolving digital landscape.
          </p>
        </div>
        <div className="mt-10 grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center">
            <div className="text-4xl font-bold text-blue-400 mb-2">500+</div>
            <p className="text-gray-400">Businesses Protected</p>
          </div>
          <div className="text-center">
            <div className="text-4xl font-bold text-blue-400 mb-2">99.9%</div>
            <p className="text-gray-400">Threat Detection Rate</p>
          </div>
          <div className="text-center">
            <div className="text-4xl font-bold text-blue-400 mb-2">24/7</div>
            <p className="text-gray-400">Expert Support</p>
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="mx-auto mb-16 max-w-6xl p-10">
        <h2 className="text-center text-3xl mb-10 text-blue-400 font-bold">
          Trusted by Industry Leaders
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="bg-slate-800 p-6 rounded-xl border border-slate-700">
            <p className="italic text-gray-300 mb-4">
              "Safe Shield has transformed our security infrastructure. Their comprehensive solution 
              detected vulnerabilities we weren't even aware of and strengthened our overall security posture."
            </p>
            <div className="flex items-center">
              <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center mr-3">
                <span className="font-bold">JD</span>
              </div>
              <div>
                <p className="font-semibold">Jane Doe</p>
                <p className="text-sm text-gray-400">CTO, Enterprise Solutions</p>
              </div>
            </div>
          </div>
          <div className="bg-slate-800 p-6 rounded-xl border border-slate-700">
            <p className="italic text-gray-300 mb-4">
              "After implementing Safe Shield, we've seen a 95% reduction in security incidents. 
              Their proactive approach to threat detection has been invaluable to our operations."
            </p>
            <div className="flex items-center">
              <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center mr-3">
                <span className="font-bold">JS</span>
              </div>
              <div>
                <p className="font-semibold">John Smith</p>
                <p className="text-sm text-gray-400">CISO, Global Tech</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="mx-auto mb-16 max-w-6xl p-10 bg-blue-900 bg-opacity-30 rounded-xl text-center">
        <h2 className="text-3xl mb-5 font-bold">Secure Your Business Today</h2>
        <p className="text-gray-300 mb-8 max-w-2xl mx-auto">
          Don't wait until you become a target. Proactive security measures save businesses
          an average of $2.5 million in breach-related costs. Start your protection plan today.
        </p>
        <div className="flex flex-col md:flex-row gap-4 justify-center">
          <button className="bg-blue-600 border-none text-white py-3 px-6 rounded-md cursor-pointer text-base font-bold hover:bg-blue-700">
            Start Free Security Assessment
          </button>
          <button className="bg-transparent border border-blue-600 text-white py-3 px-6 rounded-md cursor-pointer text-base font-bold hover:bg-blue-900">
            Schedule Consultation
          </button>
        </div>
      </section>

      {/* Footer */}
      <footer className="mx-auto max-w-6xl p-6 border-t border-slate-800 mt-10">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div className="flex items-center mb-6 md:mb-0">
            <div className="w-8 h-8 bg-blue-600 rounded-md flex items-center justify-center mr-3">
              <Shield color="white" size={16} />
            </div>
            <h3 className="text-lg font-bold text-blue-400">SafeShield</h3>
          </div>
          <div className="text-gray-400 text-sm">
            © 2025 Safe Shield. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Landing;