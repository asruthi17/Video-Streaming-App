// src/components/StreamWindow.js
import React from 'react';
import './StreamWindow.css';

export default function StreamWindow({ video, onClose }) {
  return (
    <div className="stream-window">
      <h2>Now Streaming: {video.title}</h2>
      <video width="720" height="480" controls autoPlay>
        <source src={`http://127.0.0.1:8000/stream/${video.filename}`} type="video/mp4" />
        Your browser does not support the video tag.
      </video>
      <button onClick={onClose}>Close</button>
    </div>
  );
}
