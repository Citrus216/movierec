import React from 'react';
import './ImageReel.css'; // Create this CSS file in the same directory

const Image = ({ src, alt }) => {
  return (
    <div className="image-container">
      <img src={src} alt={alt} />
    </div>
  );
};

export default Image;
