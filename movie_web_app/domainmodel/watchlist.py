from movie_web_app.A1Files.movie import Movie

class WatchList:
    def __init__(self):
        self._watchlist=[]
    def add_movie(self, movie: Movie):
        if isinstance(movie, Movie):
            if movie not in self._watchlist:
                self._watchlist.append(movie)

    def remove_movie(self, movie: Movie):
        if len(self._watchlist) !=0:
            if isinstance(movie, Movie):
                if movie in self._watchlist:
                    self._watchlist.remove(movie)

    def select_movie_to_watch(self,index):
        if index >= len(self._watchlist):
            return None
        else:
            return self._watchlist[index]

    def size(self):
        return len(self._watchlist)

    def first_movie_in_watchlist(self):
        if len(self._watchlist) !=0:
            return self._watchlist[0]
        else:
            return None

    def __iter__(self):
        return iter(self._watchlist)

    def __next__(self,list):
        if next(list)== self._watchlist[len(self._watchlist)-1]:
            StopIteration
            #print("exception")
        else:
            aa = next(list)
            return aa


class TestWatchlistMethods:
    def test_init(self):
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

        # test delete
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

        # test delete unexpected
        watchlist3 = WatchList()
        watchlist3.add_movie("Moana")
        print(watchlist3.first_movie_in_watchlist())
        assert watchlist3._watchlist == []
        watchlist3.remove_movie(Movie("Moana", 2016))
        print(f"Size of watchlist: {watchlist3.size()}")
        assert watchlist3._watchlist == []

        # select movie
        watchlist4 = WatchList()
        watchlist4.add_movie(Movie("Moana", 2016))
        ss = watchlist4.select_movie_to_watch(0)
        print(ss)

        # out of bounce
        watchlist4 = WatchList()
        watchlist4.add_movie(Movie("Moana", 2016))
        ss = watchlist4.select_movie_to_watch(10)
        print(ss)
        ##assert None

        # iterate
        watchlist5 = WatchList()
        watchlist5.add_movie(Movie("Moana", 2016))
        watchlist5.add_movie(Movie("Ice Age", 2002))
        watchlist5.add_movie(Movie("Guardians of the Galaxy", 2012))
        iterate = watchlist5.__iter__()
        print(watchlist5.__next__(iterate))
        print(watchlist5.__next__(iterate))
        # print(watchlist5.__next__(iterate))
        # print(watchlist5.__next__(iterate))




