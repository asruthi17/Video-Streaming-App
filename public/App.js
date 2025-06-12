// src/App.js
import React, { useState, useEffect } from 'react';
import LandingPage from './components/LandingPage';
import Signup from './components/Signup';
import Login from './components/Login';
import VideoList from './components/VideoList';
import CategoryTabs from './components/CategoryTabs';
import UserProfile from './components/UserProfile';
import StreamWindow from './components/StreamWindow';
import './App.css';

function App() {
  const [token, setToken] = useState(localStorage.getItem("token") || "");
  const [view, setView] = useState("landing");
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [selectedVideo, setSelectedVideo] = useState(null);

  const handleLogout = () => {
    localStorage.removeItem("token");
    setToken("");
    setView("landing");
  };

  const handleLogin = (tok) => {
    localStorage.setItem("token", tok);
    setToken(tok);
    setView("videos");
  };

  return (
    <div className="App">
      {view === "landing" && <LandingPage onNavigate={setView} />}
      {view === "signup" && <Signup onNavigate={setView} />}
      {view === "login" && <Login onLogin={handleLogin} />}
      {view === "videos" && (
        <>
          <button className="logout" onClick={handleLogout}>Logout</button>
          <UserProfile token={token} />
          <CategoryTabs onSelect={setSelectedCategory} />
          <VideoList
            token={token}
            category={selectedCategory}
            onPlay={setSelectedVideo}
          />
        </>
      )}
      {selectedVideo && (
        <StreamWindow video={selectedVideo} onClose={() => setSelectedVideo(null)} />
      )}
    </div>
  );
}

export default App;
