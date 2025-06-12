// src/components/CategoryTabs.js
import React, { useEffect, useState } from 'react';
import './CategoryTabs.css';

export default function CategoryTabs({ onSelect }) {
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/categories")
      .then((res) => res.json())
      .then(setCategories);
  }, []);

  return (
    <div className="tabs">
      <button onClick={() => onSelect(null)}>All</button>
      {categories.map((cat, idx) => (
        <button key={idx} onClick={() => onSelect(cat)}>{cat}</button>
      ))}
    </div>
  );
}
