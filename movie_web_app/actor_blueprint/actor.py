from flask import Blueprint, render_template, url_for, request

from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from flask_paginate import Pagination
from flask_paginate import Pagination, get_page_parameter
import movie_web_app.utilities.utilities as utilities
from movie_web_app.domainmodel.read_title import read_title

from flask import request, render_template, redirect, url_for, session
import movie_web_app.adapters.repository as repo
from better_profanity import profanity
import movie_web_app.utilities.utilities as utilities
import movie_web_app.actor_blueprint.services as services
from movie_web_app.authentication.authentication import login_required


actor_blueprint = Blueprint(
    'actor_bp', __name__
)


@actor_blueprint.route('/actors')
def list_actor():
    actors = repo.repo_instance.get_actors()
    per_page = 30
    a=1
    actor_list = []
    actor_index =[]
    for actor in actors:
        actor_list.append(actor)
        actor_index.append(a)
        a+=1
    total = len(actor_list)
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * per_page
    end = start + per_page
    pagination = Pagination(bs_version=3, per_page= per_page, page=page, total=total)
    actor_per_page = actor_list[start:end]

    # for actor in actor_per_page:
    #     actor['view_review_url'] = url_for('movie_bp.movies_by_year', name=actor, view_reviews_for=actor['id'])
    #     actor['add_review_url'] = url_for('movie_bp.review_on_movie', actor=actor['id'])


    return render_template(
        'others/list_actor.html',
        home_url=url_for('home_bp.home'),
        list_movie_url=url_for('movie_bp.movies_by_year'),
        list_actor_url=url_for('actor_bp.list_actor'),
        list_director_url=url_for('director_bp.list_director'),
        list_genre_url=url_for('genre_bp.list_genre'),
        search_url=url_for('search_bp.find_movie'),
        register_url= url_for('authentication_bp.register'),
        selected_movies=utilities.get_selected_movies(),
        actors=actor_per_page,
        ids=actor_index,
        pagination=pagination
    )

@actor_blueprint.route('/review', methods=['GET', 'POST'])
@login_required
def review_on_actor():
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

