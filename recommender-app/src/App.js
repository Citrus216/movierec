import React, { useState } from 'react';
import SearchBox from './components/SearchBox';
import Image from './components/ImageReel';
import Image2 from './components/ImageReel2';
import './App.css'; 
import MovieEntry from './components/MovieEntry'
import LoadingSpinner from './components/LoadingSpinner';


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
  const [ text, setText ] = useState("");
  const [ movies, setMovies ] = useState([]);
  const [ isLoading, setIsLoading ] = useState(false);

  const onChange = (event) => {
    setText(event.target.value);
  }

  const onSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      console.log(text)
      const response = await fetch(`http://127.0.0.1:5000/api/v1/movies?query=${encodeURIComponent(text)}`);

      if (response.ok) {
        const data = await response.json();
        setMovies(data.movies);
      } else {
        console.error('Failed to fetch movies');
        console.log("test")
      }
    } catch (error) {
      console.error('Error during movie fetch:', error);
      console.log("test");
    }
    setIsLoading(false);
  };

  return (
    <div className="app-container">
      <div style={{ display:"flex", flexDirection:"row", flexBasis: "9", textAlign: "center"}}>
        <Image src="https://icons.iconarchive.com/icons/icons8/ios7/256/Photo-Video-Film-Reel-Filled-icon.png" />
        <h1 style={{flex: 5, marginBottom: "30px"}}>CineMatch</h1>
        <Image2 src="https://icons.iconarchive.com/icons/icons8/ios7/256/Photo-Video-Film-Reel-Filled-icon.png" />
      </div>
      <SearchBox text={text} onChange={onChange} onSubmit={onSubmit} />

      <div className="movie-container">
        {movies.map((movie, index) => (
            <MovieEntry key={index} movie={movie} />
          ))}
      </div>
      <LoadingSpinner isLoading={isLoading} />
    </div>
  );
}

export default App;
