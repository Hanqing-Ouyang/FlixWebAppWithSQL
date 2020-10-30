from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime,
    ForeignKey
)
from sqlalchemy.orm import mapper, relationship

from movie_web_app.domainmodel import director
from movie_web_app.domainmodel import actor
# from movie_web_app.domainmodel import genre
from movie_web_app.domainmodel import model

metadata = MetaData()

users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)

reviews = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
    Column('movie_id', ForeignKey('movies.id')),
    Column('review_text', String(1024), nullable=False),
    Column('timestamp', DateTime, nullable=False)
)

movies = Table(
    'movies', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String(255), nullable=False),
    # Column('genres', String(255), nullable=True),
    Column('description', String(255), nullable=False),
    # Column('director', String(255), nullable=True),
    # Column('actors', String(1024), nullable=True),
    Column('year', Integer, nullable=False),
    # Column('Runtime (Minutes)', Integer, nullable=True),
    # Column('Rating', Integer, nullable=True),
    # Column('Votes', Integer, nullable=True),
    # Column('Revenue (Millions)', Integer, nullable=True),
    # Column('Metascore', Integer, nullable=True),
)

genres = Table(
    'genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('genre_name', String(64), nullable=False)
)

movie_genres = Table(
    'movie_genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('movie_id', ForeignKey('movies.id')),
    Column('genre_id', ForeignKey('genres.id'))
)

# directors = Table(
#     'directors', metadata,
#     Column('id', Integer, primary_key=True, autoincrement=True),
#     Column('director_full_name', String(64), nullable=False)
# )
#
# movie_director = Table(
#     'movie_director', metadata,
#     Column('id', Integer, primary_key=True, autoincrement=True),
#     Column('movie_id', ForeignKey('movies.id')),
#     Column('director_id', ForeignKey('directors.id'))
# )
#
# actors = Table(
#     'actors', metadata,
#     Column('id', Integer, primary_key=True, autoincrement=True),
#     Column('actor_full_name', String(64), nullable=False)
# )
#
# movie_actors = Table(
#     'movie_actors', metadata,
#     Column('id', Integer, primary_key=True, autoincrement=True),
#     Column('movie_id', ForeignKey('movies.id')),
#     Column('actor_id', ForeignKey('actors.id'))
# )


def map_model_to_tables():
    mapper(model.User, users, properties={
        '_username': users.columns.username,
        '_password': users.columns.password,
        '_reviews': relationship(model.Review, backref='_user')
    })
    mapper(model.Review, reviews, properties={
        '_review_text': reviews.columns.review_text,
        '_timestamp': reviews.columns.timestamp
    })


    genres_mapper = mapper(model.Genre, genres, properties={
        '_genre_name': genres.columns.genre_name,
        # '_genreged_movies': relationship(
        #     movies_mapper,
        #     secondary=movie_genres,
        #     backref="_genres"
        # )
    })

    mapper(model.Movie, movies, properties={
        '_year': movies.columns.year,
        '_title': movies.columns.title,
        '_id': movies.columns.id,
        '_description': movies.columns.description,
        '_genres': relationship(
            genres_mapper,
            secondary=movie_genres,
            backref='_genred_movies'
        ),
        '_reviews': relationship(model.Review, backref='_movie'),
        # '_actors' : movies.columns.actors,
        # '_director': movies.columns.director,
    })


    # mapper(actor.Actor, actors, properties={
    #     '_actor_full_name': actors.c.actor_full_name,
    #     '_movie_actors': relationship(
    #         movies_mapper,
    #         secondary=movie_actors,
    #         backref="_actors"
    #     )
    # })
    # mapper(director.Director, directors, properties={
    #     '_director_full_name': directors.c.director_full_name,
    #     '_movie_director': relationship(
    #         movies_mapper,
    #         secondary=movie_director,
    #         backref="_director"
    #     )
    # })