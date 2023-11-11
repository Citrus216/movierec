from sys import argv
from api import TMDBInterface, Movie, MovieList

def main(argv: list):
    interface = TMDBInterface("eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmNzFjYTJkZmQ1NTBkODQ4MDMzNmVkNjVjOGU3NmFjNSIsInN1YiI6IjY"
                              "1NGUzZjY0NjdiNjEzMDEzYzRiOWVkMyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.OG-DDQ82"
                              "Az4fl39RZiZxYowMZV1kqceKpGkLd6EIJ6M")
    get_rec(interface)


def get_rec(interface: TMDBInterface, input: str = "", pages: int = 500) -> None:
    args = {
        "page": "1"
    }
    movies = []
    fp = open("results.txt", "w")
    for i in range(1, pages + 1):
        print(i)
        args["page"] = f"{i}"
        response_json = interface.get_movie_data(args).json()
        movies.extend(response_json['results'])

    MovieList(movie_list=[Movie(json_object=movie) for movie in movies]).to_csv("results")


if __name__ == "__main__":
    main(argv)
