import requests
import csv

_URL = "https://api.themoviedb.org/3/"


class Movie:
    def __init__(self, json_object=None, prop_tuple: tuple = None):
        def try_set(key: str):
            try:
                return json_object[key]
            except KeyError:
                return None

        if json_object is not None:
            self.adult = try_set('adult')
            self.genre_ids = try_set('genre_ids')
            self.original_language = try_set('original_language')
            self.overview = try_set('overview')
            self.popularity = try_set('popularity')
            self.release_date = try_set('release_date')
            self.title = try_set('title')
            self.vote_average = try_set('vote_average')
            self.vote_count = try_set('vote_count')
            self.reviews = try_set('reviews')
        elif prop_tuple is not None:
            self.adult, self.genre_ids, self.original_language, self.overview, self.popularity, self.release_date, \
                self.title, self.vote_average, self.vote_count, self.reviews = prop_tuple
        else:
            raise Exception("Must pass in JSON or tuple to Movie")

    def get_props(self) -> tuple:
        return self.adult, self.genre_ids, self.original_language, self.overview, self.popularity, \
            self.release_date, self.title, self.vote_average, self.vote_count, self.reviews

    def __str__(self):
        return f"{self.title} {self.overview} {self.reviews}"


class MovieList:
    def __init__(self, csv_filename: str = "", movie_list: list[Movie] = None):
        if csv_filename != "":
            self.__list: list[Movie] = []
            with open(csv_filename, newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for row in reader:
                    self.__list.append(Movie(prop_tuple=tuple(row)))
        elif movie_list is not None:
            self.__list: list[Movie] = movie_list
        else:
            raise Exception("Must pass in CSV filename or list of Movies")
        for movie in self.__list:
            if any([prop is None or prop == "" for prop in movie.get_props()]) or movie.original_language != "en":
                self.__list.remove(movie)

    def to_csv(self, filename: str):
        fp = open(filename + ".csv", "w")
        csv.writer(fp, delimiter=',').writerows([movie.get_props() for movie in self.__list])

    def __getitem__(self, item):
        return self.__list[item]

    def __len__(self):
        return len(self.__list)

    def __iter__(self):
        return iter(self.__list)


class TMDBInterface:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self._DEF_HEADERS = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    def discover(self, args: dict[str, str]):
        args_str = "&".join([f"{key}={value}" for key, value in args.items()])
        return requests.get(f"{_URL}/discover/movie?{args_str}", headers=self._DEF_HEADERS)

    def get_reviews(self, movie_id: int, args: dict[str, str]):
        args_str = "&".join([f"{key}={value}" for key, value in args.items()])
        return requests.get(f"{_URL}/movie/{movie_id}/reviews?{args_str}", headers=self._DEF_HEADERS)
