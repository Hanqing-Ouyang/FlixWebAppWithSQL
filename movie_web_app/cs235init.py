from movie_web_app.datafilereaders.movie_file_csv_reader import MovieFileCSVReader
from movie_web_app.domainmodel.read_title import read_title


def main():
    filename = 'datafiles/Data1000Movies.csv'
    movie_file_reader = MovieFileCSVReader(filename)
    movie_file_reader.read_csv_file()
    movie_file_reader2 = read_title(filename)
    aa=movie_file_reader2.dataset_of_movie_titles()
    print(movie_file_reader2.dataset_of_movie_titles())
    assert isinstance(aa, list)

    print(f'number of unique movies: {len(movie_file_reader.dataset_of_movies)}')
    assert len(movie_file_reader.dataset_of_movies)== 1000
    print(f'number of unique actors: {len(movie_file_reader.dataset_of_actors)}')
    assert len(movie_file_reader.dataset_of_actors) == 1985

    print(f'number of unique directors: {len(movie_file_reader.dataset_of_directors)}')
    assert len(movie_file_reader.dataset_of_directors) ==644
    print(f'number of unique genres: {len(movie_file_reader.dataset_of_genres)}')
    assert len(movie_file_reader.dataset_of_genres) ==20

    print(movie_file_reader.dataset_of_movies)
    print(movie_file_reader.dataset_of_actors)
    print(movie_file_reader.dataset_of_directors)
    print(movie_file_reader.dataset_of_genres)
    print(movie_file_reader.dataset_of_movies[0].id)
    #print(movie_file_reader2.dataset_of_movie_titles)



#if __name__ == "__main__":
    #main()