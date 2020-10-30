from movie_web_app.A1Files.user import User, Review, Movie
from movie_web_app.domainmodel.watchlist import WatchList
from movie_web_app.activitysimulations.watchingsimulation import MovieWatchingSimulation
def main():

    movie = Movie("Moana", 2016)
    review_text = "This movie was very enjoyable."
    rating = 8
    review = Review(movie, review_text, rating)
    review2 = Review("Moana", " Moana ", 0)
    print(review2)
    assert repr(review2.movie)== "<Movie None, None>"
    assert repr(review2.review_text) == "'Moana'"
    assert repr(review2.rating) == "None"

    review3= Review(23, 23, -5)
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
    assert type(review_text)== str

    print("Rating: {}".format(review.rating))
    assert repr(review.rating) == "8"
    print(review.timestamp)
    #assert repr(review.datetime)

    # test size() & first
    watchlist = WatchList()
    print(f"Size of watchlist: {watchlist.size()}")
    assert len(watchlist._watchlist) == 0
    watchlist.add_movie(Movie("Moana", 2016))
    watchlist.add_movie(Movie("Ice Age", 2002))
    watchlist.add_movie(Movie("Guardians of the Galaxy", 2012))
    print(watchlist.first_movie_in_watchlist())
    assert watchlist._watchlist[0] == Movie("Moana", 2016)

    # test add one already have movie
    watchlist1 = WatchList()
    watchlist1.add_movie(Movie("Moana", 2016))
    watchlist1.add_movie(Movie("Moana", 2016))
    print(f"Size of watchlist: {watchlist1.size()}")
    assert len(watchlist1._watchlist) == 1
    print(watchlist1.first_movie_in_watchlist())
    assert watchlist1._watchlist[0] == Movie("Moana", 2016)

    #test delete
    watchlist2 = WatchList()
    print(f"Size of watchlist: {watchlist2.size()}")
    assert len(watchlist2._watchlist) == 0
    watchlist2.remove_movie(Movie("Moana", 2016))
    print(f"Size of watchlist: {watchlist2.size()}")
    assert len(watchlist2._watchlist) == 0
    watchlist2.add_movie(Movie("Moana", 2016))
    print(f"Size of watchlist: {watchlist2.size()}")
    assert len(watchlist2._watchlist) == 1
    watchlist2.remove_movie(Movie("Moana", 2016))
    print(f"Size of watchlist: {watchlist2.size()}")
    assert len(watchlist2._watchlist) == 0

    #test delete unexpected
    watchlist3 = WatchList()
    watchlist3.add_movie("Moana")
    print(watchlist3.first_movie_in_watchlist())
    assert watchlist3._watchlist == []
    watchlist3.remove_movie(Movie("Moana", 2016))
    print(f"Size of watchlist: {watchlist3.size()}")
    assert watchlist3._watchlist == []

    #select movie
    watchlist4 = WatchList()
    watchlist4.add_movie(Movie("Moana", 2016))
    ss=watchlist4.select_movie_to_watch(0)
    print(ss)

    #out of bounce
    watchlist4 = WatchList()
    watchlist4.add_movie(Movie("Moana", 2016))
    ss = watchlist4.select_movie_to_watch(10)
    print(ss)
    ##assert None

    #iterate
    watchlist5 = WatchList()
    watchlist5.add_movie(Movie("Moana", 2016))
    watchlist5.add_movie(Movie("Ice Age", 2002))
    watchlist5.add_movie(Movie("Guardians of the Galaxy", 2012))
    iterate= watchlist5.__iter__()
    print(watchlist5.__next__(iterate))
    print(watchlist5.__next__(iterate))
    #print(watchlist5.__next__(iterate))
    #print(watchlist5.__next__(iterate))

    #test MovieWatchingSimulation
    mws=MovieWatchingSimulation()
    movie=Movie("moana",2016)
    user=User('Martin', 'pw12345')
    comment1=mws.make_review("I like it",8,movie,user)
    print(comment1)
    print(movie._comments)
    print(user._reviews)
    result= mws.delete_comment("I like it",movie,user)
    print(result)
    print(movie._comments)
    print(user._reviews)




if __name__ == "__main__":
        main()