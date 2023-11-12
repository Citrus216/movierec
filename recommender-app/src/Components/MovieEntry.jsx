// MovieEntry.tsx
import React from 'react';
import './MovieEntry.css';
import RecommendationScore from './RecommendationScore';

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
    vote_average,
    vote_count,
    sim_score,
    rec_score,
    image_url,
  } = movie;

  return (
    <div className="movie-entry">
      <div className="left-column">
        <img className="movie-image" src={image_url} alt={`Poster for ${title}`} />
      </div>
      <div className="right-column">
        <h2>{title}</h2>
        <h3>Rating: {vote_average}</h3>
        <h3>Number of Ratings: {vote_count}</h3>
      </div>
      <RecommendationScore className="recommendation" recScore={Math.round(rec_score)} simScore={Math.round(sim_score)} />
    </div>
  );
};

export default MovieEntry;
