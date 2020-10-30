import csv
from movie_web_app.domainmodel.model import Movie
from movie_web_app.domainmodel.actor import Actor
from movie_web_app.domainmodel.model import Genre
from movie_web_app.domainmodel.director import Director
from movie_web_app.domainmodel.read_title import read_title


class MovieFileCSVReader:

    def __init__(self, file_name: str):
        self.__file_name = file_name


    def read_csv_file(self):
        with open(self.__file_name, mode='r', encoding='utf-8-sig') as csvfile:
            movie_file_reader = csv.DictReader(csvfile)
            index = 0
            for row in movie_file_reader:
                title = row['Title']
                release_year = int(row['Year'])
                index += 1

    @property
    def dataset_of_movies(self) -> list:
        with open(self.__file_name, mode='r', encoding='utf-8-sig') as csvfile:
            movie_file_reader = csv.DictReader(csvfile)
            index = 0
            movies=[]
            for row in movie_file_reader:
                new_movie = Movie(row['Title'],int(row['Year']))
                new_movie.director = Director(row['Director'])
                gn=[]
                for a in row['Genre'].split(","):
                    temp=Genre(a.strip())
                    gn.append(temp)
                new_movie.genres = gn
                ac=[]
                for a in row['Actors'].split(","):
                    temp=Actor(a.strip())
                    ac.append(temp)
                new_movie.actors = ac
                new_movie.id = int(row['Rank'])
                new_movie.runtime_minutes = int(row['Runtime (Minutes)'])
                new_movie.description = row['Description']
                movies.append(new_movie)
                index += 1
            return list(movies)

    @property
    def dataset_of_actors(self) -> list():
        with open(self.__file_name, mode='r', encoding='utf-8-sig') as csvfile:
            movie_file_reader = csv.DictReader(csvfile)
            index = 0
            actors= list()
            for row in movie_file_reader:
                for a in row['Actors'].split(","):
                    temp=Actor(a.strip())
                    if temp not in actors:
                        actors.append(temp)
                index += 1
            actors.sort(key=lambda x: x.actor_full_name, reverse=False)
            return list(actors)

    @property
    def dataset_of_directors(self) -> list():
        with open(self.__file_name, mode='r', encoding='utf-8-sig') as csvfile:
            movie_file_reader = csv.DictReader(csvfile)
            index = 0
            directors_set = set()
            directors=list()
            for row in movie_file_reader:
                directors_set.add(Director(row['Director']))
                index += 1
            for a in directors_set:
                directors.append(a)
            directors.sort(key=lambda x: x.director_full_name, reverse=False)
            return list(directors)

    @property
    def dataset_of_genres(self) -> list():
        with open(self.__file_name, mode='r', encoding='utf-8-sig') as csvfile:
            movie_file_reader = csv.DictReader(csvfile)
            index = 0
            genres = list()
            for row in movie_file_reader:
                for g in row['Genre'].split(","):
                    temp=Genre(g.strip())
                    if temp not in genres:
                        genres.append(temp)
                index += 1
            return list(genres)


class TestFileReaderMethods:

    def test_init(self):
        filename = 'datafiles/Data1000Movies.csv'
        movie_file_reader = MovieFileCSVReader(filename)
        movie_file_reader.read_csv_file()
        movie_file_reader2 = read_title(filename)
        aa = movie_file_reader2.dataset_of_movie_titles()
        print(movie_file_reader2.dataset_of_movie_titles())
        assert isinstance(aa, list)

        print(f'number of unique movies: {len(movie_file_reader.dataset_of_movies)}')
        assert len(movie_file_reader.dataset_of_movies) == 1000
        print(f'number of unique actors: {len(movie_file_reader.dataset_of_actors)}')
        assert len(movie_file_reader.dataset_of_actors) == 1985

        print(f'number of unique directors: {len(movie_file_reader.dataset_of_directors)}')
        assert len(movie_file_reader.dataset_of_directors) == 644
        print(f'number of unique genres: {len(movie_file_reader.dataset_of_genres)}')
        assert len(movie_file_reader.dataset_of_genres) == 20

        print(movie_file_reader.dataset_of_movies)
        print(movie_file_reader.dataset_of_actors)
        print(movie_file_reader.dataset_of_directors)
        print(movie_file_reader.dataset_of_genres)

        # print(movie_file_reader2.dataset_of_movie_titles)

