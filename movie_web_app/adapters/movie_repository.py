import abc
import csv
import os
from typing import List
from datetime import datetime
from bisect import bisect, bisect_left, insort_left
from werkzeug.security import generate_password_hash

# from movie_web_app.domainmodel.movie import Movie
from movie_web_app.domainmodel.director import Director
from movie_web_app.domainmodel.actor import Actor
# from movie_web_app.domainmodel.genre import Genre
from movie_web_app.domainmodel.model import User,Review,Movie,make_review,Genre
# from movie_web_app.domainmodel.review import Review
from movie_web_app.adapters.repository import AbstractRepository, RepositoryException
from movie_web_app.datafilereaders.movie_file_csv_reader import MovieFileCSVReader


class MainRepository(AbstractRepository):

    def __init__(self):
        self._movies: List[Movie] = list()
        self._movies_index = dict()
        self._actors: List[Actor] = list()
        self._directors: List[Director] = list()
        self._genres: List[Genre] = list()
        self._users: List[User] = list()
        self._reviews: List[Review] = list()
        self._years: List[int] = list()
        self._watchlist: List[Movie] = list()
        self._watchlist_dict= dict()


    # def __iter__(self):
    #     self._current = 0
    #     return self

    def get_users(self):
        return self._users

    # def __next__(self):
    #     if self._current >= len(self._movies):
    #         raise StopIteration
    #     else:
    #         self._current += 1
    #         return self._movies[self._current-1]

    def add_movies(self, movies:list):
        for movie in movies:
            self._movies.append(movie)
            self._movies_index[movie.id] = movie
            if movie.year not in self._years:
                self._years.append(movie.year)


    def add_actors(self, actors:list):
        for actor in actors:
            self._actors.append(actor)

    def add_genres(self, genres:list):
        for genre in genres:
            self._genres.append(genre)

    def add_directors(self, directors:list):
        for director in directors:
            self._directors.append(director)

    def get_movies(self):
        return self._movies

    def get_actors(self):
        return self._actors

    def get_genres(self):
        return self._genres

    def get_directors(self):
        return self._directors

    def add_movie(self, movie:Movie):
        movie.id = len(self._movies)+1
        if movie.year not in self._years:
            self._years.append(movie.year)
        insort_left(self._movies, movie)
        self._movies_index[movie.id] = movie

    def get_result(self, title: str) -> list:
        ##return Actor(title)
        title=title.title().strip()
        movies=[]
        for movie in self._movies:
            if movie.title == title or \
                    Actor(title) in movie.actors or \
                    movie.director == Director(title) or \
                    Genre(title) in movie.genres:
                movies.append(movie)
        return movies

    def get_movie(self, id: int) -> Movie:
        movie = None

        try:
            movie = self._movies_index[id]
        except KeyError:
            pass  # Ignore exception and return None.

        return movie

    def add_director(self, director: Director):
        self._directors.append(director)

    def get_director(self, director_full_name: str):
        return next((director for director in self._directors if director.director_full_name == director_full_name), None)

    def add_actor(self, actor: Actor):
        self._actors.append(actor)

    def get_actor(self, actor_full_name: str):
        return next((actor for actor in self._actors if actor.actor_full_name == actor_full_name), None)

    def add_genre(self, genre: Genre):
        self._genres.append(genre)

    def get_genre(self, genre_name) -> Genre:
        return next((genre for genre in self._genres if genre.genre_name == genre_name), None)

    def add_user(self, user: User):
        self._users.append(user)
        self._watchlist_dict[user]=[]
        # print(user)
        # print(self._users)

    def get_user(self, username) -> User:
        # print(username)
        # print("get_user",next((user for user in self._users if user.username == username.title()), None))
        return next((user for user in self._users if user.username == username.title()), None)

    def add_users(self, users:list):
        for user in users:
            self._users.append(user)

    def get_users(self):
        return self._users

    def get_number_of_movies(self):
        return len(self._movies)

    def get_movies_by_id(self, id_list):
        # Strip out any ids in id_list that don't represent movie ids in the repository.
        existing_ids = [id for id in id_list if id in self._movies_index]

        # Fetch the movies.
        movies = [self._movies_index[id] for id in existing_ids]
        return movies

    # Helper method to return movie index.
    def movie_index(self, movie: Movie):
        index = bisect_left(self._movies, movie)
        if index != len(self._movies) and self._movies[index].year == movie.year:
            return index
        raise ValueError

    def get_movie_ids_for_genre(self, genre_name: str):
        movies = []
        for movie in self._movies:
            if Genre(genre_name) in movie.genres:
                movies.append(movie.id)
        return movies

    def get_year_of_previous_movie(self, movie: Movie):
        # previous_year = None
        years = []
        self._years.sort()

        try:
            index = self._years.index(movie.year)

            if index-1 <0:
                return None
            else:
                years.append(self._years[index - 1])
                return years[0]

        except ValueError:
            # No articles for specified date. Simply return an empty list.
            return None


    def get_year_of_next_movie(self, movie: Movie):
        # index = None
        years = []
        self._years.sort()
        try:
            index= self._years.index(movie.year)
            if index+1 >= len(self._years):
                return None
            else:
                years.append(self._years[index + 1])

                return years[0]
        except ValueError:
            # No articles for specified date. Simply return an empty list.
            return None
        # return self._years



    def get_movies_by_year(self, target_year: int) -> List[Movie]:
        # target_movie = Movie(
        #     title=None,
        #     year=target_year,
        # )
        matching_movies = list()

        for movie in self._movies:
            if int(movie.year) == target_year:
                matching_movies.append(movie)

        return matching_movies

    def add_review(self, review: Review):
        super().add_review(review)
        self._reviews.append(review)

    def get_reviews(self):
        return self._reviews

    def get_first_movie(self) -> Movie:
        movie = None

        if len(self._movies) > 0:
            movie = self._movies[0]
        return movie

    def get_last_movie(self) -> Movie:
        movie = None

        if len(self._movies) > 0:
            movie = self._movies[-1]
        return movie

    def add_favorite_movie(self, user: User, movie: Movie):
        user.watch_movie(movie)
        if user in self._watchlist_dict.keys():
            if movie not in self._watchlist_dict.values():
                self._watchlist_dict[user].append(movie)

    def get_watchlist(self,user):
        return self._watchlist_dict[user]

    # def get_movie_id_for_watchlist(self,movie:Movie) ->list:
    #     movies = []
    #     for movie in self._movies:
    #         if Genre(genre_name) in movie.genres:
    #             movies.append(movie.id)
    #     return movies

def read_csv_file(filename: str):
    with open(filename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Read first line of the the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row

def load_movies(data_path: str, repo: MainRepository):
    movies = dict()

    for data_row in read_csv_file(data_path + '/Data1000Movies.csv'):
        movie = Movie(
            title=data_row[1],
            year=int(data_row[6]),
        )
        movie.director = Director(data_row[4])
        gn = []
        for a in data_row[2].split(","):
            temp = Genre(a.strip())
            gn.append(temp)
        movie.genres = gn
        ac = []
        for a in data_row[5].split(","):
            temp = Actor(a.strip())
            ac.append(temp)
        movie.actors = ac
        movie.id = int(data_row[0])
        movie.runtime_minutes = int(data_row[7])
        movie.description = data_row[3]
        repo.add_movie(movie)
        movies[data_row[0]] = movie
    return movies

def load_users(data_path: str, repo: MainRepository):
    users = dict()

    for data_row in read_csv_file(data_path + '/users.csv'):
        user = User(
            username=data_row[1],
            password=generate_password_hash(data_row[2])
        )
        repo.add_user(user)
        users[data_row[0]] = user
    return users

def load_reviews(data_path: str, repo: MainRepository, users):
    for data_row in read_csv_file(os.path.join(data_path,'comments.csv')):
        review = make_review(
            review_text=data_row[3],
            user=users[data_row[1]],
            movie=repo.get_movie(int(data_row[2])),
            timestamp=datetime.fromisoformat(data_row[4])
        )

        repo.add_review(review)
        
    

def populate(data_path: str, repo: MainRepository):
    # # Load articles and tags into the repository.
    # load_articles_and_tags(data_path, repo)
    load_movies(data_path, repo)
    # Load users into the repository.
    users = load_users(data_path, repo)

    # Load reviews into the repository.
    load_reviews(data_path, repo, users)


    