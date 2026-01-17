'use client';

import { useState, useEffect } from 'react';
import axios from 'axios';

// API Base URL
const API_BASE = 'http://localhost:8000';

interface HealthStatus {
  status: string;
  message?: string;
}

export default function Home() {
  const [healthStatus, setHealthStatus] = useState<HealthStatus | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check API health on mount
    axios.get(`${API_BASE}/health`)
      .then(res => {
        setHealthStatus(res.data);
        setLoading(false);
      })
      .catch(() => {
        setHealthStatus({ status: 'offline', message: 'Backend not running' });
        setLoading(false);
      });
  }, []);

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="pt-24 pb-16 text-center relative overflow-hidden">
        {/* Animated Background Orbs */}
        <div className="absolute w-96 h-96 rounded-full bg-[radial-gradient(circle,rgba(99,102,241,0.3)_0%,transparent_70%)] -top-24 -left-24 animate-float -z-10" />
        <div className="absolute w-72 h-72 rounded-full bg-[radial-gradient(circle,rgba(244,114,182,0.2)_0%,transparent_70%)] -bottom-12 -right-12 animate-float [animation-direction:reverse] [animation-duration:8s] -z-10" />

        <div className="max-w-4xl mx-auto px-4">
          {/* Logo & Title */}
          <h1 className="text-5xl md:text-7xl font-extrabold mb-4 gradient-text animate-gradient">
            Wevolve
          </h1>

          <p className="text-xl text-text-secondary mb-8 font-light max-w-xl mx-auto">
            The AI-Powered Career Acceleration Ecosystem
          </p>

          {/* API Status Badge */}
          <div className={`inline-block px-4 py-2 rounded-full border mb-12 ${loading
              ? 'border-text-muted text-text-muted'
              : healthStatus?.status === 'healthy'
                ? 'border-green-500 text-green-500'
                : 'border-red-500 text-red-500'
            }`}>
            {loading ? 'Connecting...' : healthStatus?.status === 'healthy' ? '🟢 Backend Connected' : '🔴 Backend Offline'}
          </div>
        </div>
      </section>

      {/* Feature Cards */}
      <section className="max-w-6xl mx-auto px-4 pb-20">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Resume Intelligence */}
          <div className="glass-card p-8 transition-all duration-300 hover:-translate-y-2 hover:shadow-[0_20px_40px_rgba(99,102,241,0.3)]">
            <div className="w-16 h-16 rounded-xl bg-gradient-to-br from-wevolve-primary to-wevolve-primary-light flex items-center justify-center mb-6 shadow-[0_8px_24px_rgba(99,102,241,0.4)]">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold mb-3">Resume Intelligence</h3>
            <p className="text-text-secondary text-sm mb-4">
              Upload your resume and get instant AI-powered parsing with confidence scores. Know exactly how complete your profile is.
            </p>
            <span className="inline-block px-3 py-1 text-xs border border-wevolve-primary text-wevolve-primary rounded-full">
              The Fix
            </span>
          </div>

          {/* Transparent Matching */}
          <div className="glass-card p-8 transition-all duration-300 hover:-translate-y-2 hover:shadow-[0_20px_40px_rgba(244,114,182,0.3)]">
            <div className="w-16 h-16 rounded-xl bg-gradient-to-br from-wevolve-secondary to-pink-300 flex items-center justify-center mb-6 shadow-[0_8px_24px_rgba(244,114,182,0.4)]">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold mb-3">Transparent Matching</h3>
            <p className="text-text-secondary text-sm mb-4">
              See exactly why you match with a job. Our multi-factor engine explains every score: Skills (40%), Location, Salary, and more.
            </p>
            <span className="inline-block px-3 py-1 text-xs border border-wevolve-secondary text-wevolve-secondary rounded-full">
              The Why
            </span>
          </div>

          {/* Actionable Growth */}
          <div className="glass-card p-8 transition-all duration-300 hover:-translate-y-2 hover:shadow-[0_20px_40px_rgba(34,211,238,0.3)]">
            <div className="w-16 h-16 rounded-xl bg-gradient-to-br from-wevolve-accent to-cyan-300 flex items-center justify-center mb-6 shadow-[0_8px_24px_rgba(34,211,238,0.4)]">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path d="M12 14l9-5-9-5-9 5 9 5z" />
                <path d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 14l9-5-9-5-9 5 9 5zm0 0l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14zm-4 6v-7.5l4-2.222" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold mb-3">Actionable Growth</h3>
            <p className="text-text-secondary text-sm mb-4">
              Get a personalized learning roadmap based on your skill gaps. We show you how to become the perfect candidate.
            </p>
            <span className="inline-block px-3 py-1 text-xs border border-wevolve-accent text-wevolve-accent rounded-full">
              The How
            </span>
          </div>
        </div>

        {/* CTA Button */}
        <div className="text-center mt-16">
          <button className="px-10 py-4 text-lg font-semibold text-white rounded-lg bg-gradient-to-r from-wevolve-primary to-wevolve-secondary shadow-[0_8px_24px_rgba(99,102,241,0.4)] transition-all duration-300 hover:scale-105 hover:shadow-[0_12px_32px_rgba(99,102,241,0.5)]">
            🚀 Start Your Evolution
          </button>
          <p className="text-text-secondary text-sm mt-4">
            Upload your resume to get started →
          </p>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 text-center border-t border-white/10 mt-auto">
        <p className="text-text-secondary text-sm">
          Built with ❤️ by <strong>Kasukabe Defence Group</strong>
        </p>
      </footer>
    </div>
  );
}
