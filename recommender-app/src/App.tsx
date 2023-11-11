import React, { useState, ChangeEvent } from 'react';

const App = () => {
  const [searchTerm, setSearchTerm] = useState('');

  const handleSearchChange = (e: ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
  };

  return (
    <div style={{ textAlign: 'center', marginTop: '50px' }}>
      <h1>Movie Recommender</h1>
      <input
        type="text"
        placeholder="Search for movies..."
        value={searchTerm}
        onChange={handleSearchChange}
        style={{ padding: '10px', margin: '10px', width: '80%' }}
      />
      <p>You are searching for: {searchTerm}</p>
      {/* Add your movie recommendation logic or display here */}
    </div>
  );
};

export default App;

