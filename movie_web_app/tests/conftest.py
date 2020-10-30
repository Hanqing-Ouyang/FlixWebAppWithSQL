import os
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from movie_web_app.adapters.orm import metadata, map_model_to_tables

from movie_web_app import create_app
from movie_web_app.adapters.movie_repository import MainRepository
from movie_web_app.adapters import movie_repository, database_repository
import movie_web_app.adapters.movie_repository as mv_repo
from movie_web_app.datafilereaders.movie_file_csv_reader import MovieFileCSVReader


# TEST_DATA_PATH = os.path.join('C:', os.sep, 'iCloud Drive', 'Documents', 'GitHub', 'FlixSkeletonWebApp','movie_web_app', 'tests', 'data')
#TEST_DATA_PATH = os.path.join('C:', os.sep, 'Users', 'iwar006', 'Documents', 'Python dev', 'COVID-19', 'tests', 'data')
TEST_DATA_PATH_MEMORY = '/Users/takesei/Documents/GitHub/FlixWebAppWithSQL/movie_web_app/tests/data/movie'
TEST_DATA_PATH_DATABASE = '/Users/takesei/Documents/GitHub/FlixWebAppWithSQL/movie_web_app/tests/data/database'

TEST_DATABASE_URI_IN_MEMORY = 'sqlite://'
TEST_DATABASE_URI_FILE = 'sqlite:///movie_webb_app_test.db'

@pytest.fixture
def in_movie_repo():
    # filename = '/Users/takesei/Documents/GitHub/FlixSkeletonWebApp/movie_web_app/datafiles/Data1000Movies.csv'
    # movie_file_reader = MovieFileCSVReader(filename)

    # repo.repo_instance.add_movies(movie_file_reader.dataset_of_movies)
    # repo.repo_instance.add_actors(movie_file_reader.dataset_of_actors)
    # repo.repo_instance.add_directors(movie_file_reader.dataset_of_directors)
    # repo.repo_instance.add_genres(movie_file_reader.dataset_of_genres)
    repo = MainRepository()
    movie_repository.populate(TEST_DATA_PATH_MEMORY, repo)
    return repo

@pytest.fixture
def database_engine():
    engine = create_engine(TEST_DATABASE_URI_FILE)
    clear_mappers()
    metadata.create_all(engine)  # Conditionally create database tables.
    for table in reversed(metadata.sorted_tables):  # Remove any data from the tables.
        engine.execute(table.delete())
    map_model_to_tables()
    # data_filename = 'Data1000Movies.csv'
    # session_factory = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    # database_repository.populate_reader(session_factory, TEST_DATA_PATH_DATABASE, data_filename)
    database_repository.populate(engine, TEST_DATA_PATH_DATABASE)
    yield engine
    metadata.drop_all(engine)
    clear_mappers()

@pytest.fixture
def empty_session():
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(bind=engine)
    yield session_factory()
    metadata.drop_all(engine)
    clear_mappers()

@pytest.fixture
def session():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(bind=engine)
    # data_filename = 'Data1000Movies.csv'
    # # session_factory = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    # database_repository.populate_reader(session_factory, TEST_DATA_PATH_DATABASE, data_filename)
    database_repository.populate(engine, TEST_DATA_PATH_DATABASE)
    yield session_factory()
    metadata.drop_all(engine)
    clear_mappers()

@pytest.fixture
def session_factory():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(bind=engine)
    # data_filename = 'Data1000Movies.csv'
    # # session_factory = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    # database_repository.populate_reader(session_factory, TEST_DATA_PATH_DATABASE, data_filename)
    database_repository.populate(engine, TEST_DATA_PATH_DATABASE)
    yield session_factory
    metadata.drop_all(engine)
    clear_mappers()


@pytest.fixture
def client():
    my_app = create_app({
        'TESTING': True,  # Set to True during testing.
        'REPOSITORY': 'movie',  # Set to 'memory' or 'database' depending on desired repository.
        'TEST_DATA_PATH': TEST_DATA_PATH_MEMORY,  # Path for loading test data into the repository.
        'WTF_CSRF_ENABLED': False  # test_client will not send a CSRF token, so disable validation.
    })

    return my_app.test_client()


class AuthenticationManager:
    def __init__(self, client):
        self._client = client

    def login(self, username='thorke', password='cLQ^C#oFXloS'):
        return self._client.post(
            'authentication/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthenticationManager(client)
