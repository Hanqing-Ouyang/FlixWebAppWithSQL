from movie_web_app.A1Files.user import User, Review, Movie
from movie_web_app.datafilereaders.movie_file_csv_reader import MovieFileCSVReader

class MovieWatchingSimulation:
    pass

    def __init__(
            self,
    ):
        self._movies= MovieFileCSVReader.dataset_of_movies


    def make_review(self,comment:str,rating:int,movie:Movie,user:User):
        if isinstance(comment, str) and isinstance(rating, int) and isinstance(user, User) and isinstance(movie, Movie):
                review=Review(movie,comment,rating)
                movie.add_comment(comment)
                user.add_review(review)
                return review


    def delete_comment(self,comment:str,movie:Movie,user:User):
        if comment in movie._comments:
            movie.remove_comment(comment)
            for re in user._reviews:
                if comment == re._review_text:
                    user.remove_review(comment,movie)
            return "comment deleted"

class TestMovieWatchingSimulationMethods:

    def test_init(self):
        mws = MovieWatchingSimulation()
        movie = Movie("moana", 2016)
        user = User('Martin', 'pw12345')
        comment1 = mws.make_review("I like it", 8, movie, user)
        print(comment1)
        print(movie._comments)
        print(user._reviews)
        result = mws.delete_comment("I like it", movie, user)
        print(result)
        print(movie._comments)
        print(user._reviews)