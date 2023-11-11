from typing import List
from sys import argv

import nltk
from nltk.tokenize import word_tokenize
from api import MovieList, Movie
from re import sub
import csv
from sklearn.decomposition import TruncatedSVD

nltk.download('punkt')


# pass over the movie list and get the synopsis for each movie. clean them.
# create embeddings.csv with word, *embedding vector. Should be about 15kx15k
# from embeddings.csv, create numpy matrix
# from numpy matrix, create movie matrix by totalling embedding matrices of words in the movie synopsis


class MovieVector:
    def __init__(self, movie: Movie, vector: list[float]):
        self.movie = movie
        self.vector = vector

    def __getitem__(self, item):
        return self.vector[item]

    def __len__(self):
        return len(self.vector)

    def __iter__(self):
        return iter(self.vector)

    def normalize(self):
        total = sum([abs(val) for val in self.vector]) + 1
        self.vector = [val / total for val in self.vector]
        return self


def compare(vector1: MovieVector, vector2: MovieVector, norm: int = 1):
    return sum([abs(vector1[i] - vector2[i]) ** norm for i in range(len(vector1))]) ** (1 / norm)


# splits into a list of lists of words with inner lists being sentences
def tokenize_synopsis(synopsis: str) -> list[list[str]]:
    # for now just use their tokenizer
    sentences = synopsis.split(". ")
    sentences = [sub(r"[!-,.-/:-@[-`{-~\-—]", " ", sentence).lower() for sentence in sentences]
    sentences = [word_tokenize(sentence) for sentence in sentences]
    return sentences


def tokenize_synopses(movies: MovieList) -> list[list[list[str]]]:
    synopses = [movie.overview for movie in movies]
    synopses = [tokenize_synopsis(synopsis) for synopsis in synopses]
    return synopses


def to_embeddings(synopses: list[list[list[str]]]) -> dict[str, list[float]]:
    embeddings = {}
    words = []
    for synopsis in synopses:
        for sentence in synopsis:
            for word in sentence:
                if word not in embeddings.keys():
                    embeddings[word] = None
                    words.append(word)

    for word in embeddings.keys():
        embeddings[word] = [0] * len(words)

    print(len(words), "words")

    for synopsis in synopses:
        for sentence in synopsis:
            for word in sentence:
                for other_word in sentence:
                    if word != other_word:
                        embeddings[word][words.index(other_word)] += 1
                print("done with", word)

    matrix_rep = [array for _, array in embeddings.items()]
    svd = TruncatedSVD(n_components=200)
    transformed = svd.fit_transform(matrix_rep)
    for word in words:
        embeddings[word] = transformed[words.index(word)]

    orig_embeddings_writer = csv.writer(open("orig_embeddings.csv", "w"))
    for word in embeddings.keys():
        orig_embeddings_writer.writerow([word, *embeddings[word]])

    print("done with svd")

    writer = csv.writer(open("embeddings.csv", "w"))

    # normalize embeddings
    for word in embeddings.keys():
        total = sum([abs(val) for val in embeddings[word]]) + 1
        embeddings[word] = embeddings[word] / total
        writer.writerow([word, *embeddings[word]])
        print("done with normalization of", word)

    return embeddings


def calc_movie_vectors(embeddings: dict[str, list[float]], synopses: list[list[list[str]]]) -> List[list[float]]:
    movie_vectors = []
    for synopsis in synopses:
        movie_vector = [0] * len(embeddings[list(embeddings.keys())[0]])
        for sentence in synopsis:
            for word in sentence:
                movie_vector += embeddings[word]
        movie_vectors.append(movie_vector)
    return movie_vectors


def get_movie_vectors(movies: MovieList) -> tuple[dict[str, list[float]], list[MovieVector]]:
    synopses = tokenize_synopses(movies)
    embeddings = to_embeddings(synopses)
    movie_vectors = calc_movie_vectors(embeddings, synopses)
    return embeddings, [MovieVector(movie, vector).normalize() for movie, vector in zip(movies, movie_vectors)]


def main():
    csv_filename = "results.csv"
    movie_list = MovieList(csv_filename=csv_filename)
    embeddings, movie_vectors = get_movie_vectors(movie_list)
    writer = csv.writer(open("movie_vectors.csv", "w"))
    for i, movie_vector in enumerate(movie_vectors):
        writer.writerow([movie_vector.movie.title, *movie_vector.vector])

    # compare similarity of movies that should be similar and dissimilar
    nun_vector = movie_vectors[16]
    print(nun_vector.movie.title)
    exorcist_vector = movie_vectors[18]
    print(exorcist_vector.movie.title)
    meg_vector = movie_vectors[20]
    print(meg_vector.movie.title)
    pp_vector = movie_vectors[17]
    print(pp_vector.movie.title)
    print("nun and exorcist:", compare(nun_vector, exorcist_vector, 2))
    print("nun and meg", compare(nun_vector, meg_vector, 2))
    print("nun and pp", compare(nun_vector, pp_vector, 2))

    print("'horror' and nun", compare(embeddings['horror'], nun_vector, 2))
    print("'horror' and pp", compare(embeddings['horror'], pp_vector, 2))
    print("'horror' and exorcist", compare(embeddings['horror'], exorcist_vector, 2))

    user_input = input("Enter a description: ")
    total_vector = [0] * len(embeddings[list(embeddings.keys())[0]])
    for word in word_tokenize(user_input):
        total_vector += embeddings[word]
    print('user input and nun', compare(total_vector, nun_vector, 2))
    print('user input and pp', compare(total_vector, pp_vector, 2))
    print('user input and exorcist', compare(total_vector, exorcist_vector, 2))
    print('user input and meg', compare(total_vector, meg_vector, 2))

    print("done")


if __name__ == "__main__":
    main()
