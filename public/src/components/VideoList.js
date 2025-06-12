// src/components/VideoList.js
import React, { useEffect, useState } from 'react';
import './VideoList.css';

export default function VideoList({ token, category, onPlay }) {
  const [videos, setVideos] = useState([]);

  useEffect(() => {
    let url = "http://127.0.0.1:8000/videos";
    if (category) url += `?category=${category}`;

    fetch(url)
      .then((res) => res.json())
      .then(setVideos)
      .catch(console.error);
  }, [category]);

  return (
    <div className="video-list">
      <h2>Available Videos</h2>
      {videos.map((video) => (
        <div key={video.id} className="video-card">
          <h3>{video.title}</h3>
          <p>Category: {video.category}</p>
          <button onClick={() => onPlay(video)}>Play</button>
        </div>
      ))}
    </div>
  );
}
