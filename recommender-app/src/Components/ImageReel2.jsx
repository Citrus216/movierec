import React from 'react';
import './ImageReel2.css'; // Create this CSS file in the same directory

const Image = ({ src, alt }) => {
  return (
    <div className="image2-container">
      <img src={src} alt={alt} />
    </div>
  );
};

export default Image;
