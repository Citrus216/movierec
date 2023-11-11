import React, { useState } from 'react';
import './SearchBox.css'; // Create this CSS file in the same directory

const SearchBox = () => {
  const [searchTerm, setSearchTerm] = useState('');

  const handleSearchChange = (event) => {
    setSearchTerm(event.target.value);
  };

  const handleSearchSubmit = (event) => {
    event.preventDefault();
    // You can perform search-related actions here with the 'searchTerm'
    console.log('Search Term:', searchTerm);
  };

  return (
    <div className="search-container">
      <form onSubmit={handleSearchSubmit}>
        <input
          type="text"
          placeholder="Search..."
          value={searchTerm}
          onChange={handleSearchChange}
        />
        <button type="submit">
          <img
            src="https://cdn-icons-png.flaticon.com/512/61/61088.png"
            alt="Search"
          />
        </button>
      </form>
    </div>
  );
};

export default SearchBox;
