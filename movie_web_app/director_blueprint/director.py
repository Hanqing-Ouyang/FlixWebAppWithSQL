from flask import Blueprint, render_template, url_for, request

from flask_paginate import Pagination
from flask_paginate import Pagination, get_page_parameter
import movie_web_app.utilities.utilities as utilities
from movie_web_app.domainmodel.read_title import read_title

import movie_web_app.adapters.repository as repo


director_blueprint = Blueprint(
    'director_bp', __name__
)


@director_blueprint.route('/directors')
def list_director():
    directors = repo.repo_instance.get_directors()
    per_page = 30
    a = 1
    director_list = []
    director_index = []
    for director in directors:
        director_list.append(director)
        director_index.append(a)
        a += 1
    total = len(director_list)
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * per_page
    end = page * per_page if total > page * per_page else total
    pagination = Pagination(bs_version=3, per_page=per_page, page=page, total=total)
    director_per_page = director_list[start:end]

    return render_template(
        'others/list_director.html',
        home_url=url_for('home_bp.home'),
        list_movie_url=url_for('movie_bp.movies_by_year'),
        list_actor_url=url_for('actor_bp.list_actor'),
        list_director_url=url_for('director_bp.list_director'),
        list_genre_url=url_for('genre_bp.list_genre'),
        search_url=url_for('search_bp.find_movie'),
        register_url=url_for('authentication_bp.register'),
        directors=director_per_page,
        ids=director_index,
        pagination=pagination,
        selected_movies=utilities.get_selected_movies(),

    )

