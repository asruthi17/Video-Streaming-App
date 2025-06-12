// src/components/LandingPage.js
import React from 'react';
import './LandingPage.css';

export default function LandingPage({ onNavigate }) {
  return (
    <div className="landing">
      <h1>🎬 Welcome to StreamZone</h1>
      <button onClick={() => onNavigate("login")}>Login</button>
      <button onClick={() => onNavigate("signup")}>Sign Up</button>
    </div>
  );
}
