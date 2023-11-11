// MovieEntry.tsx
import React from 'react';
import './MovieEntry.css';

// interface Movie {
//   title: string;
//   rating: number;
//   numRatings: number;
//   recommendedScore: number;
//   similarityScore: number;
//   imageUrl: string;
// }

// interface MovieEntryProps {
//   movie: Movie;
// }

const MovieEntry = ({ movie }) => {
  const {
    title,
    rating,
    numRatings,
    recommendedScore,
    similarityScore,
    imageUrl,
  } = movie;

  return (
    <div className="movie-entry">
      <div className="left-column">
        <img src={imageUrl} alt={`Poster for ${title}`} />
      </div>
      <div className="right-column">
        <h2>{title}</h2>
        <p>Rating: {rating}</p>
        <p>Number of Ratings: {numRatings}</p>
        <p>Recommended Score: {recommendedScore}</p>
        <p>Similarity Score: {similarityScore}</p>
      </div>
    </div>
  );
};

export default MovieEntry;
