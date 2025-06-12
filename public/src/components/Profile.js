import React from 'react';

function Profile() {
  const username = localStorage.getItem('token');

  return (
    <div className="container">
      <h2>User Profile</h2>
      <p>Username: {username}</p>
    </div>
  );
}

export default Profile;
