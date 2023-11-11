import React from 'react';
import SearchBox from './Components/SearchBox';
import Image from './Components/ImageReel';
import Image2 from './Components/ImageReel2';
import './App.css'; 
import MovieEntry from './Components/MovieEntry'


const moviesData = [
  // Replace this with your actual movie data
  {
    title: 'Movie 1',
    rating: 4.5,
    numRatings: 100,
    recommendedScore: 8.2,
    similarityScore: 0.75,
    imageUrl: 'https://example.com/poster1.jpg',
  },
  {
    title: 'Movie 2',
    rating: 3.8,
    numRatings: 75,
    recommendedScore: 7.5,
    similarityScore: 0.65,
    imageUrl: 'https://example.com/poster2.jpg',
  },
  // Add more movies as needed
  {
    title: 'Movie 3',
    rating: 4.0,
    numRatings: 35,
    recommendedScore: 6.5,
    similarityScore: 0.85,
    imageUrl: 'https://example.com/poster2.jpg',
  },
];

function App() {
  return (
    <div className="app-container">
      <h1>CineMatch</h1>
      <SearchBox />
      {/* Other components and content */}
      <Image src="https://icons.iconarchive.com/icons/icons8/ios7/256/Photo-Video-Film-Reel-Filled-icon.png" />
      <Image2 src="https://icons.iconarchive.com/icons/icons8/ios7/256/Photo-Video-Film-Reel-Filled-icon.png" />

      <div className="movie-container">
        {moviesData.map((movie, index) => (
            <MovieEntry key={index} movie={movie} />
          ))}

      </div>
    </div>
  );
}

export default App;
