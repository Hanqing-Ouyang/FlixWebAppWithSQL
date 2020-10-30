import csv

class read_title:
    def __init__(self, file_name: str):
        self.__file_name = file_name

    def dataset_of_movie_titles(self):
        with open(self.__file_name, mode='r', encoding='utf-8-sig') as csvfile:
            movie_file_reader = csv.DictReader(csvfile)
            index = 0
            titles = []
            for row in movie_file_reader:
                new_title = row['Title']
                titles.append(new_title)
                index += 1
            return list(titles)