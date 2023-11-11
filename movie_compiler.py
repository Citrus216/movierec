from sys import argv
from api import TMDBInterface, Movie, MovieList
from pprint import pprint
from json import loads

def main(argv: list):
    interface = TMDBInterface("eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmNzFjYTJkZmQ1NTBkODQ4MDMzNmVkNjVjOGU3NmFjNSIsInN1YiI6IjY"
                              "1NGUzZjY0NjdiNjEzMDEzYzRiOWVkMyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.OG-DDQ82"
                              "Az4fl39RZiZxYowMZV1kqceKpGkLd6EIJ6M")
    if len(argv) > 1:
        get_rec(interface, pages=int(argv[1]))
    else:
        get_rec(interface)


def get_rec(interface: TMDBInterface, pages: int = 500) -> None:
    args = {
        "page": "1"
    }
    movies = []
    for i in range(1, pages + 1):
        print(i)
        args["page"] = f"{i}"
        response_json = interface.discover(args).json()
        try:
            for movie in response_json['results']:
                reviews_json = interface.get_reviews(movie['id'], {}).json()
                results = reviews_json['results']
                movie['reviews'] = " ".join([review['content'] for review in results])
        except Exception:
            print("exception")
            pass
        try:
            for movie in response_json['results']:
                if len(movie['reviews'].split(" ") + movie['overview'].split(" ")) < 100:
                    continue
                movies.append(movie)
        except KeyError:
            pprint(response_json)
            continue

    movie_list = MovieList(movie_list=[Movie(json_object=movie) for movie in movies])
    movie_list.to_csv("results")


if __name__ == "__main__":
    main(argv)
