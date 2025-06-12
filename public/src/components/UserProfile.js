// src/components/UserProfile.js
import React from 'react';
import './UserProfile.css';

export default function UserProfile({ token }) {
  return (
    <div className="user-profile">
      <p>🔐 Logged in as: <strong>{token}</strong></p>
    </div>
  );
}
