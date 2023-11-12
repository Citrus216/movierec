import React, { useState } from 'react';
import './SearchBox.css'; // Create this CSS file in the same directory

const SearchBox = ({ text, onChange, onSubmit }) => {
//
//   const handleSearchChange = (event) => {
//     setSearchTerm(event.target.value);
//   };
//
//   const handleSearchSubmit = (event) => {
//     event.preventDefault();
//     // You can perform search-related actions here with the 'searchTerm'
//     console.log('Search Term:', searchTerm);
//   };

  return (
    <div className="search-container">
      <form onSubmit={onSubmit}>
        <input
          type="text"
          placeholder="Search..."
          value={text}
          onChange={onChange}
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
