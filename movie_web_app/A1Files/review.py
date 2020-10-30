from datetime import datetime
from movie_web_app.A1Files.movie import Movie

class Review:

    def __init__(
        self, movie: Movie, review_text: str
    ):
        if not isinstance(movie, Movie):
            self._movie= Movie("None",None)
        else:
            self._movie = movie
        if type(review_text) is str:
            self._review_text = review_text.strip()
        else:
            self._review_text =None

        self._rating = None
        self._timestamp = datetime.now()


    @property
    def movie(self) -> "Movie":
        return self._movie

    @movie.setter
    def movie(self, movie):
        if isinstance(movie, Movie):
            self._movie = movie

    @property
    def rating(self) -> int:
        return self._rating

    @rating.setter
    def rating(self, rating):
        if rating <= 10 and rating >= 1:
            self._rating = rating
        else:
            self._rating = None

    @property
    def review_text(self) -> str:
        return self._review_text

    @review_text.setter
    def review_text(self, review_text):
        if type(review_text) is  str:
            self._review_text = review_text.strip()

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        if isinstance(timestamp, datetime):
            self._timestamp = timestamp

    def __repr__(self):
        return f'<Review {self._movie}, {self._review_text}, {self._rating}, {self._timestamp}>'

    def __eq__(self, other):
        if not isinstance(other, Review):
            return False
        return (
                other._movie == self._movie and
                other._review_text == self._review_text and
                other._rating == self._rating and
                other._timestamp == self._timestamp
        )

class TestReviewMethods:

    def test_init(self):
        movie = Movie("Moana", 2016)
        review_text = "This movie was very enjoyable."
        rating = 8
        review = Review(movie, review_text, rating)
        review2 = Review("Moana", " Moana ", 0)
        print(review2)
        assert repr(review2.movie) == "<Movie None, None>"
        assert repr(review2.review_text) == "'Moana'"
        assert repr(review2.rating) == "None"

        review3 = Review(23, 23, -5)
        print(review3)
        assert repr(review3.movie) == "<Movie None, None>"
        assert repr(review3.review_text) == "None"
        assert repr(review3.rating) == "None"
        print(movie)
        assert repr(movie) == "<Movie Moana, 2016>"
        print(review.movie)
        assert repr(review.movie) == "<Movie Moana, 2016>"
        print("Review: {}".format(review.review_text))
        assert repr(review.review_text) == "'This movie was very enjoyable.'"
        assert type(review_text) == str

        print("Rating: {}".format(review.rating))
        assert repr(review.rating) == "8"
        print(review.timestamp)
        # assert repr(review.datetime)