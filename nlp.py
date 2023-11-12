from typing import List
from sys import argv

import nltk
from nltk.tokenize import word_tokenize
from api import MovieList, Movie
from re import sub
import csv
from sklearn.decomposition import TruncatedSVD
import math

nltk.download('punkt')


# pass over the movie list and get the synopsis for each movie. clean them.
# create embeddings.csv with word, *embedding vector. Should be about 15kx15k
# from embeddings.csv, create numpy matrix
# from numpy matrix, create movie matrix by totalling embedding matrices of words in the movie synopsis


EMBEDDINGS_FILE = "embeddings.csv"
MOVIE_VECTORS_FILE = "movie_vectors.csv"


class MovieVector:
    def __init__(self, movie: Movie, vector: list[float]):
        self.movie = movie
        self.vector = vector

    def __getitem__(self, item):
        try:
            return self.vector[item]
        except IndexError:
            return 0

    def __len__(self):
        return len(self.vector)

    def __iter__(self):
        return iter(self.vector)

    def normalize(self):
        total = math.sqrt(sum([val * val for val in self.vector]))
        self.vector = [val / total for val in self.vector]
        return self


def compare(vector1: MovieVector, vector2: MovieVector, norm: int = 1):
    return sum([abs(vector1[i] - vector2[i]) ** norm for i in range(len(vector1))]) ** (1 / norm)


# splits into a list of lists of words with inner lists being sentences
def tokenize(synopsis: str) -> list[list[str]]:
    # for now just use their tokenizer
    sentences = synopsis.split(". ")
    sentences = [sub(r"[!-,.-/:-@[-`{-~\-—]", " ", sentence).lower() for sentence in sentences]
    sentences = [word_tokenize(sentence) for sentence in sentences]
    for i, sentence in enumerate(sentences):
        for j, word in enumerate(sentence):
            # use nltk for stemming
            # word = nltk.PorterStemmer().stem(word)
            sentences[i][j] = word

    return sentences


def tokenize_movies(movies: MovieList) -> list[list[list[str]]]:
    synopses = [str(movie) for movie in movies]
    synopses = [tokenize(synopsis) for synopsis in synopses]
    return synopses


def to_embeddings(synopses: list[list[list[str]]]) -> dict[str, list[float]]:
    matrix_rep = []
    words = {}
    total = 0
    print("starting to fill words")
    for synopsis in synopses:
        for sentence in synopsis:
            for word in sentence:
                if word not in words:
                    matrix_rep.append(None)
                    words[word] = total
                    total += 1

    for i in range(total):
        matrix_rep[i] = [0] * total

    print(total, "words")

    print("starting to fill embeddings")
    for synopsis in synopses:
        for sentence in synopsis:
            for word in sentence:
                for other_word in sentence:
                    if word != other_word:
                        matrix_rep[words[word]][words[other_word]] += 1

    print("Starting SVD")
    svd = TruncatedSVD(n_components=100)
    transformed = svd.fit_transform(matrix_rep)
    embeddings = {}
    for word in words:
        embeddings[word] = transformed[words[word]]

    print("writing embeddings")
    orig_embeddings_writer = csv.writer(open("orig_embeddings.csv", "w"))
    for word in words.keys():
        orig_embeddings_writer.writerow([word, *embeddings[word]])

    writer = csv.writer(open("embeddings.csv", "w"))

    # print("normalizing embeddings")
    # # normalize embeddings
    for word in words.keys():
        #     total = sum([abs(val) for val in embeddings[word]]) + 1
        #     embeddings[word] = embeddings[word] / total
        writer.writerow([word, *embeddings[word]])

    print("done")
    return embeddings


def calc_movie_vectors(embeddings: dict[str, list[float]], synopses: list[list[list[str]]]) -> List[list[float]]:
    movie_vectors = []
    for synopsis in synopses:
        movie_vector = [0] * len(embeddings["the"])
        for sentence in synopsis:
            for word in sentence:
                if word in embeddings:
                    for i in range(len(movie_vector)):
                        movie_vector[i] += embeddings[word][i]
        # for word in title:
        #     if word in embeddings.keys():
        #         movie_vector += embeddings[word] * title_weight
        movie_vectors.append(movie_vector)
    return movie_vectors


def get_movie_vectors(movies: MovieList, recalc: bool = True) -> tuple[dict[str, list[float]], list[MovieVector]]:
    synopses = tokenize_movies(movies)
    if not recalc:
        with open(EMBEDDINGS_FILE, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            embeddings = {row[0]: [float(val) for val in row[1:]] for row in reader}
    else:
        embeddings = to_embeddings(synopses)
    if not recalc:
        with open(MOVIE_VECTORS_FILE, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            movie_vectors = [[float(val) for val in row[1:]] for row in reader]
    else:
        movie_vectors = calc_movie_vectors(embeddings, synopses)
    return embeddings, [MovieVector(movie, vector).normalize() for movie, vector in zip(movies, movie_vectors)]


def get_rec_score(movie: Movie, sim_score: float) -> float:
    return (float(movie.vote_average) + sim_score) / 1.1


def get_recommendations(input: str, recalc: bool = True) -> list[dict]:
    ret = []

    csv_filename = "results.csv"
    movie_list = MovieList(csv_filename=csv_filename)
    embeddings, movie_vectors = get_movie_vectors(movie_list, recalc=recalc)

    # total_vector = [0] * len(embeddings[list(embeddings.keys())[0]])
    total_vector = [0] * len(embeddings["the"])
    for sentence in tokenize(input):
        for word in sentence:
            for i in range(len(total_vector)):
                if word in embeddings:
                    total_vector[i] += embeddings[word][i]

    total_vector = MovieVector(None, total_vector).normalize()

    similarities: dict[Movie, float] = {}
    for movie_vector in movie_vectors:
        similarities[movie_vector.movie] = compare(total_vector, movie_vector, norm=2)

    max_sim = max(similarities.values())
    similarities = {movie: max_sim - similarity for movie, similarity in similarities.items()}
    max_sim = max(similarities.values())
    similarities = {movie: similarity / max_sim for movie, similarity in similarities.items()}

    for movie, similarity in similarities.items():
        ret.append({
            'title': movie.title,
            'vote_average': movie.vote_average,
            'vote_count': movie.vote_count,
            'sim_score': similarity * 100,
            'rec_score': get_rec_score(movie, similarity * 100),
            'image_url': f"https://image.tmdb.org/t/p/w500{movie.poster_path}",
        })

    ret = sorted(ret, key=lambda item: item['rec_score'], reverse=True)[:50]
    return ret

def main():
    csv_filename = "results.csv"
    movie_list = MovieList(csv_filename=csv_filename)
    embeddings, movie_vectors = get_movie_vectors(movie_list, recalc=True)
    writer = csv.writer(open("movie_vectors.csv", "w"))
    for i, movie_vector in enumerate(movie_vectors):
        writer.writerow([movie_list[i].title, *movie_vector])

    # compare similarity of movies that should be similar and dissimilar

    while True:
        try:
            user_input = input("Enter a description: ")
            total_vector = [0] * len(embeddings[list(embeddings.keys())[0]])
            for sentence in tokenize(user_input):
                for word in sentence:
                    for i in range(len(total_vector)):
                        if word in embeddings.keys():
                            total_vector[i] += embeddings[word][i]

            total_vector = MovieVector(None, total_vector).normalize()

            similarities: dict[str, float] = {}
            for movie_vector in movie_vectors:
                similarities[movie_vector.movie.title] = compare(total_vector, movie_vector, norm=2)

            print("Top 10 recommendations:")
            for movie, similarity in sorted(similarities.items(), key=lambda item: item[1])[:50]:
                print(movie, similarity)
        except IndexError:
            break

    print("done")


if __name__ == "__main__":
    main()
