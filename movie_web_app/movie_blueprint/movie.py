from flask import Blueprint, render_template, url_for, request

from flask import request, render_template, redirect, url_for, session

from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

from flask_paginate import Pagination
from flask_paginate import Pagination, get_page_parameter
from movie_web_app.domainmodel.read_title import read_title

import movie_web_app.adapters.repository as repo
import movie_web_app.utilities.utilities as utilities
import movie_web_app.movie_blueprint.services as services
from movie_web_app.authentication.authentication import login_required


movie_blueprint = Blueprint(
    'movie_bp', __name__
)


# @movie_blueprint.route('/movies')
# def list_movie():
#     # movies = repo.repo_instance.get_movies()
#     # per_page=10
#     # movie_list = []
#     # for movie in movies:
#     #     movie_list.append(movie)
#     # total=len(movie_list)
#     # page=request.args.get(get_page_parameter(),type=int, default=1)
#     # start=(page-1)*per_page
#     # end= start+per_page
#     # pagination= Pagination(bs_version=3, page=page, total=total)
#     # movie_per_page= movie_list[start:end]
#
#     return render_template(
#         'movies/list_movie.html',
#         home_url=url_for('home_bp.home'),
#         list_movie_url=url_for('movie_bp.list_movie'),
#         list_actor_url=url_for('actor_bp.list_actor'),
#         list_director_url=url_for('director_bp.list_director'),
#         list_genre_url=url_for('genre_bp.list_genre'),
#         search_url=url_for('search_bp.find_movie'),
#         register_url=url_for('authentication_bp.register'),
#         movies=movie_per_page,
#         pagination= pagination
#     )

@movie_blueprint.route('/movies_by_year', methods=['GET'])
@login_required
def movies_by_year():
    # Read query parameters.
    target_year = request.args.get('year')
    movie_to_show_reviews = request.args.get('view_reviews_for')

    # Fetch the first and last movies in the series.
    first_movie = services.get_first_movie(repo.repo_instance)
    last_movie = services.get_last_movie(repo.repo_instance)

    if target_year is None:
        # No year query parameter, so return movies from day 1 of the series.
        target_year = first_movie['year']
    else:
        # Convert target_year from string to year.
        target_year = int(target_year)

    if movie_to_show_reviews is None:
        # No view-reviews query parameter, so set to a non-existent movie id.
        movie_to_show_reviews = -1
    else:
        # Convert movie_to_show_reviews from string to int.
        movie_to_show_reviews = int(movie_to_show_reviews)

    # Fetch movie(s) for the target year. This call also returns the previous and next years for movies immediately
    # before and after the target year.
    movies, previous_year, next_year = services.get_movies_by_year(target_year, repo.repo_instance)

    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    if len(movies) > 0:
        # There's at least one movie for the target year.
        if previous_year is not None:
            # There are movies on a previous year, so generate URLs for the 'previous' and 'first' navigation buttons.
            prev_movie_url = url_for('movie_bp.movies_by_year', year=previous_year)
            first_movie_url = url_for('movie_bp.movies_by_year', year=2006)

        # There are movies on a subsequent year, so generate URLs for the 'next' and 'last' navigation buttons.
        if next_year is not None:
            next_movie_url = url_for('movie_bp.movies_by_year', year=next_year)
            last_movie_url = url_for('movie_bp.movies_by_year', year=last_movie['year'])

        # Construct urls for viewing movie reviews and adding reviews.
        username=session['username']
        for movie in movies:
            movie['view_review_url'] = url_for('movie_bp.movies_by_year', year=target_year, view_reviews_for=movie['id'])
            movie['add_review_url'] = url_for('movie_bp.review_on_movie', movie=movie['id'])
            movie['add_to_watchlist_url'] = url_for('movie_bp.add_to_watchlist', user=username, movie=movie['id'])

        # Generate the webpage to display the movies.
        return render_template(
            'movies/list_movie.html',
            title='movies',
            movies_title=target_year,
            movies=movies,
            selected_movies=utilities.get_selected_movies(6),
            genre_urls=utilities.get_genres_and_urls(),
            first_movie_url=first_movie_url,
            last_movie_url=last_movie_url,
            prev_movie_url=prev_movie_url,
            next_movie_url=next_movie_url,
            show_reviews_for_movie=movie_to_show_reviews,
        )

    # No movies to show, so return the homepage.
    return redirect(url_for('home_bp.home'))


@movie_blueprint.route('/movies_by_genre', methods=['GET'])
@login_required
def movies_by_genre():
    movies_per_page = 10

    # Read query parameters.
    genre_name = request.args.get('genre')
    cursor = request.args.get('cursor')
    movie_to_show_reviews = request.args.get('view_reviews_for')

    if movie_to_show_reviews is None:
        # No view-reviews query parameter, so set to a non-existent movie id.
        movie_to_show_reviews = -1
    else:
        # Convert movie_to_show_reviews from string to int.
        movie_to_show_reviews = int(movie_to_show_reviews)

    if cursor is None:
        # No cursor query parameter, so initialise cursor to start at the beginning.
        cursor = 0
    else:
        # Convert cursor from string to int.
        cursor = int(cursor)

    # Retrieve movie ids for movies that are genreged with genre_name.
    movie_ids = services.get_movie_ids_for_genre(genre_name, repo.repo_instance)

    # Retrieve the batch of movies to display on the Web page.
    movies = services.get_movies_by_id(movie_ids[cursor:cursor + movies_per_page], repo.repo_instance)

    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    if cursor > 0:
        # There are preceding movies, so generate URLs for the 'previous' and 'first' navigation buttons.
        prev_movie_url = url_for('movie_bp.movies_by_genre', genre=genre_name, cursor=cursor - movies_per_page)
        first_movie_url = url_for('movie_bp.movies_by_genre', genre=genre_name)

    if cursor + movies_per_page < len(movie_ids):
        # There are further movies, so generate URLs for the 'next' and 'last' navigation buttons.
        next_movie_url = url_for('movie_bp.movies_by_genre', genre=genre_name, cursor=cursor + movies_per_page)

        last_cursor = movies_per_page * int(len(movie_ids) / movies_per_page)
        if len(movie_ids) % movies_per_page == 0:
            last_cursor -= movies_per_page
        last_movie_url = url_for('movie_bp.movies_by_genre', genre=genre_name, cursor=last_cursor)

    # Construct urls for viewing movie reviews and adding reviews.
    username = session['username']
    for movie in movies:
        movie['view_review_url'] = url_for('movie_bp.movies_by_genre', genre=genre_name, cursor=cursor, view_reviews_for=movie['id'])
        movie['add_review_url'] = url_for('movie_bp.review_on_movie', movie=movie['id'])
        movie['add_to_watchlist_url'] = url_for('movie_bp.movies_in_watchlist', user=username, movie=movie['id'])

    # Generate the webpage to display the movies.
    return render_template(
        'movies/list_movie.html',
        title='movies',
        movies_title='movies genreged by ' + genre_name,
        movies=movies,
        selected_movies=utilities.get_selected_movies(len(movies)),
        genre_urls=utilities.get_genres_and_urls(),
        first_movie_url=first_movie_url,
        last_movie_url=last_movie_url,
        prev_movie_url=prev_movie_url,
        next_movie_url=next_movie_url,
        show_reviews_for_movie=movie_to_show_reviews,
    )


@movie_blueprint.route('/add', methods=['GET'])
@login_required
def add_to_watchlist():
    movie_id = int(request.args.get('movie'))
    username = session['username']
    movie= services.get_movie(movie_id,repo.repo_instance)
    user = repo.repo_instance.get_user(username)
    services.add_movie_to_watchlist(username, movie_id, repo.repo_instance)
    user.watch_movie(movie)
    print("add to watchlist now")
    print("this is movie id", movie_id)
    print("user", user.watched_movies)
    print(services.get_watchlist_for_user(username,repo.repo_instance))
    # print(services.get_watchlist(repo.repo_instance))
    print("user", user)
    return redirect(url_for('movie_bp.movies_by_year', year=movie['year']))

@movie_blueprint.route('/watchlist', methods=['GET', 'POST'])
@login_required
def movies_in_watchlist():
    movies_per_page = 10

    # Read query parameters.
    # genre_name = request.args.get('genre')
    # movie_id = int(request.args.get('movie'))
    username = session['username']
    cursor = request.args.get('cursor')
    movie_to_show_reviews = request.args.get('view_reviews_for')
    # services.add_movie_to_watchlist(username, movie_id, repo.repo_instance)
    user = repo.repo_instance.get_user(username)
    # print("this is movie id", movie_id)
    # print(user.watched_movies)
    # print("user",user)

    if movie_to_show_reviews is None:
        # No view-reviews query parameter, so set to a non-existent movie id.
        movie_to_show_reviews = -1
    else:
        # Convert movie_to_show_reviews from string to int.
        movie_to_show_reviews = int(movie_to_show_reviews)

    if cursor is None:
        # No cursor query parameter, so initialise cursor to start at the beginning.
        cursor = 0
    else:
        # Convert cursor from string to int.
        cursor = int(cursor)

    # Retrieve movie ids for movies that are genreged with genre_name.

    movies_list = services.get_watchlist_for_user(username,repo.repo_instance)
    movie_ids = services.get_movie_ids(movies_list)
    # Movie Dict
    # movies = services.get_movies_by_id(movie_ids,repo.repo_instance)
    # Retrieve the batch of movies to display on the Web page.
    movies = services.get_movies_by_id(movie_ids[cursor:cursor + movies_per_page], repo.repo_instance)

    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    if cursor > 0:
        # There are preceding movies, so generate URLs for the 'previous' and 'first' navigation buttons.
        prev_movie_url = url_for('movie_bp.movies_in_watchlist', user=username, cursor=cursor - movies_per_page)
        first_movie_url = url_for('movie_bp.movies_in_watchlist', user=username)

    if cursor + movies_per_page < len(movie_ids):
        # There are further movies, so generate URLs for the 'next' and 'last' navigation buttons.
        next_movie_url = url_for('movie_bp.movies_in_watchlist', user=username, cursor=cursor + movies_per_page)

        last_cursor = movies_per_page * int(len(movie_ids) / movies_per_page)
        if len(movie_ids) % movies_per_page == 0:
            last_cursor -= movies_per_page
        last_movie_url = url_for('movie_bp.movies_in_watchlist', user=username, cursor=last_cursor)

    # Construct urls for viewing movie reviews and adding reviews.
    for movie in movies:
        movie['view_review_url'] = url_for('movie_bp.movies_in_watchlist', user=username, cursor=cursor,
                                           view_reviews_for=movie['id'])
        movie['add_review_url'] = url_for('movie_bp.review_on_movie', movie=movie['id'])

    # Generate the webpage to display the movies.
    return render_template(
        'movies/list_movie.html',
        title='My favorite movie',
        movies_title='My favorite movie',
        movies=movies,
        selected_movies=utilities.get_selected_movies(6),
        genre_urls=utilities.get_genres_and_urls(),
        first_movie_url=first_movie_url,
        last_movie_url=last_movie_url,
        prev_movie_url=prev_movie_url,
        next_movie_url=next_movie_url,
        show_reviews_for_movie=movie_to_show_reviews,
    )


@movie_blueprint.route('/review', methods=['GET', 'POST'])
@login_required
def review_on_movie():
    # Obtain the username of the currently logged in user.
    username = session['username']

    # Create form. The form maintains state, e.g. when this method is called with a HTTP GET request and populates
    # the form with an movie id, when subsequently called with a HTTP POST request, the movie id remains in the
    # form.
    form = reviewForm()

    if form.validate_on_submit():
        # Successful POST, i.e. the review text has passed data validation.
        # Extract the movie id, representing the reviewed movie, from the form.
        movie_id = int(form.movie_id.data)

        # Use the service layer to store the new review.
        services.add_review(movie_id, form.review.data, username, repo.repo_instance)

        # Retrieve the movie in dict form.
        movie = services.get_movie(movie_id, repo.repo_instance)

        # Cause the web browser to display the page of all movies that have the same year as the reviewed movie,
        # and display all reviews, including the new review.
        return redirect(url_for('movie_bp.movies_by_year', year=movie['year'], view_reviews_for=movie_id))

    if request.method == 'GET':
        # Request is a HTTP GET to display the form.
        # Extract the movie id, representing the movie to review, from a query parameter of the GET request.
        movie_id = int(request.args.get('movie'))

        # Store the movie id in the form.
        form.movie_id.data = movie_id
    else:
        # Request is a HTTP POST where form validation has failed.
        # Extract the movie id of the movie being reviewed from the form.
        movie_id = int(form.movie_id.data)

    # For a GET or an unsuccessful POST, retrieve the movie to review in dict form, and return a Web page that allows
    # the user to enter a review. The generated Web page includes a form object.
    movie = services.get_movie(movie_id, repo.repo_instance)
    return render_template(
        'movies/comment_on_movies.html',
        title='Edit movie',
        movie=movie,
        form=form,
        handler_url=url_for('movie_bp.review_on_movie'),
        selected_movies=utilities.get_selected_movies(),
        genre_urls=url_for('genre_bp.list_genre')
    )


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class reviewForm(FlaskForm):
    review = TextAreaField('review', [
        DataRequired(),
        Length(min=4, message='Your review is too short'),
        ProfanityFree(message='Your review must not contain profanity')])
    movie_id = HiddenField("movie id")
    submit = SubmitField('Submit')















