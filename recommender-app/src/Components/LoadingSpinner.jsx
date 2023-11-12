import React from 'react';
import './LoadingSpinner.css'; // You can style this as needed

const LoadingSpinner = ({ isLoading }) => {
  return isLoading ? (
    <div className="loading-overlay">
      <div className="loading-spinner"></div>
    </div>
  ) : null;
};

export default LoadingSpinner;
