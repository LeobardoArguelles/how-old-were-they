import requests, datetime
from decouple import config
from os import path

NOW = datetime.datetime.now()
YEAR = NOW.year
MONTH = NOW.month
DAY = NOW.day

IMAGE_ROOT = 'https://image.tmdb.org/t/p/'
LANGUAGE = '&language=en-US'
PROFILE_RESOLUTION = 'w185'
POSTER_RESOLUTION = 'w185'

def search_options(target, media):
    """
    Busca la película recibida.
    :param target: Película/serie a bucar
    :param media: Tipo de media: "movie" o "serie"
    :return: Tuple with a list of characters, and the official title of the
             target, or (None, None) if target was not found
    """
    API_KEY = config('KEY')
    if media == 'movie':
        ROOT = 'https://api.themoviedb.org/3/search/movie?api_key='
        is_movie = True
    else:
        ROOT = 'https://api.themoviedb.org/3/search/tv?api_key='
        is_movie = False

    # Create query
    # movie = input("What movie are you watching?\n")
    query = ROOT + API_KEY + LANGUAGE + '&query=' + target.replace(' ', '%20')
    query += '&page=1'

    # Get movie data
    data = requests.get(query).json()['results']

    if not data:
        return (None, None)

    n_results = len(data)
    i = 0
    options = []

    while (i < n_results and i < 3):
        option_data = data[i]
        i += 1

        if is_movie:
            date_field = 'release_date'
            media_kind = "movie"
        else:
            date_field = 'first_air_date'
            media_kind = "serie"

        release_year = option_data[date_field].split('-')[0]

        if option_data['poster_path']:
            movie_poster = IMAGE_ROOT + POSTER_RESOLUTION + option_data['poster_path']
        else:
            movie_poster = path.join('static', 'no-poster.jpg')

        option = {
            "id": str(option_data['id']),
            "title": option_data ['original_title'] if is_movie else option_data['name'],
            "release_year": release_year,
            "poster": movie_poster,
            "media_kind": media_kind
        }
        options.append(option)

    return (options)

def search(id, media):
    """
    Busca la película o la serie recibida, usando su <id>
    """
    API_KEY = config('KEY')
    if media == 'movie':
        ROOT = 'https://api.themoviedb.org/3/movie/'
        is_movie = True
    else:
        ROOT = 'https://api.themoviedb.org/3/tv/'
        is_movie = False

    # Create query
    # movie = input("What movie are you watching?\n")
    query = ROOT + id + "?api_key=" + API_KEY + LANGUAGE

    # Get movie data
    data = requests.get(query).json()

    if not data:
        return (None, None)

    real_title = data ['original_title'] if is_movie else data['name']
    if is_movie:
        release_date = {
          'year': int(data['release_date'].split('-')[0]),
          'month': int(data['release_date'].split('-')[1]),
          'day': int(data['release_date'].split('-')[2])
        }
    else:
        release_date = {
          'year': int(data['first_air_date'].split('-')[0]),
          'month': int(data['first_air_date'].split('-')[1]),
          'day': int(data['first_air_date'].split('-')[2])
        }
    # movie_poster = IMAGE_ROOT + POSTER_RESOLUTION + data['poster_path']

    # Get movie cast
    # 'https://api.themoviedb.org/3/tv/70523/credits?api_key=f290a6cd7f26e869cf63e412e5b1ec91&language=en-US'
    query = 'https://api.themoviedb.org/3/' + ('movie/' if is_movie else 'tv/')
    query += id + '/credits?api_key=' + API_KEY + LANGUAGE
    data = requests.get(query).json()
    cast = data['cast']

    # Get relevant data for each actor
    characters = {}
    for person in cast:
        if person["known_for_department"] != "Acting":
            continue
        person_data = requests.get('https://api.themoviedb.org/3/person/' + str(person['id']) + '?api_key=' + API_KEY + LANGUAGE).json()
        if not person_data['birthday'] or not person_data['profile_path']:
            continue
        characters[person['character']] = Person(
          person['name'],
          person_data['birthday'],
          calculate_age(Person.split_birthday(person_data['birthday']), release_date),
          person['id'],
          IMAGE_ROOT + PROFILE_RESOLUTION + person_data['profile_path']
        )

    return (characters, real_title)


# def search(target, media):
#     """
#     Busca la película recibida.
#     :param target: Película/serie a bucar
#     :param media: Tipo de media: "movie" o "serie"
#     :return: Tuple with a list of characters, and the official title of the
#              target, or (None, None) if target was not found
#     """
#     API_KEY = config('KEY')
#     if media == 'movie':
#         ROOT = 'https://api.themoviedb.org/3/search/movie?api_key='
#         is_movie = True
#     else:
#         ROOT = 'https://api.themoviedb.org/3/search/tv?api_key='
#         is_movie = False

#     # Create query
#     # movie = input("What movie are you watching?\n")
#     query = ROOT + API_KEY + LANGUAGE + '&query=' + target.replace(' ', '%20')
#     print(query)
#     query += '&page=1'

#     # Get movie data
#     data = requests.get(query).json()['results']

#     if not data:
#         return (None, None)
#     data = data[0]
#     my_id = str(data['id'])
#     real_title = data ['original_title'] if is_movie else data['name']
#     if is_movie:
#         release_date = {
#           'year': int(data['release_date'].split('-')[0]),
#           'month': int(data['release_date'].split('-')[1]),
#           'day': int(data['release_date'].split('-')[2])
#         }
#     else:
#         release_date = {
#           'year': int(data['first_air_date'].split('-')[0]),
#           'month': int(data['first_air_date'].split('-')[1]),
#           'day': int(data['first_air_date'].split('-')[2])
#         }
#     # movie_poster = IMAGE_ROOT + POSTER_RESOLUTION + data['poster_path']

#     # Get movie cast
#     # 'https://api.themoviedb.org/3/tv/70523/credits?api_key=f290a6cd7f26e869cf63e412e5b1ec91&language=en-US'
#     query = 'https://api.themoviedb.org/3/' + ('movie/' if is_movie else 'tv/')
#     query += my_id + '/credits?api_key=' + API_KEY + LANGUAGE
#     data = requests.get(query).json()
#     cast = data['cast']

#     # Get relevant data for each actor
#     characters = {}
#     for person in cast:
#         if person["known_for_department"] != "Acting":
#             continue
#         person_data = requests.get('https://api.themoviedb.org/3/person/' + str(person['id']) + '?api_key=' + API_KEY + LANGUAGE).json()
#         if not person_data['birthday'] or not person_data['profile_path']:
#             continue
#         characters[person['character']] = Person(
#           person['name'],
#           person_data['birthday'],
#           calculate_age(Person.split_birthday(person_data['birthday']), release_date),
#           person['id'],
#           IMAGE_ROOT + PROFILE_RESOLUTION + person_data['profile_path']
#         )

#     # for character, actor in characters.items():
#     #   print(f"{character} was played by {actor.name} at the age of {calculate_age(actor.birthday, release_date)}.")

#     return (characters, real_title)


def tabulate(characters):
    """
    Helper function for debugging.
    """
    id_width = 10
    name_width = 25
    age_width = 4
    print('ID'.center(id_width) + '|' + 'NAME'.center(name_width) + '|' + 'AGE'.center(age_width))
    for character in characters.values():
        print('|'.join(
          [
            character.id.ljust(id_width),
            character.name.ljust(name_width),
            (character.age if character.age else "NaN").center(age_width)
          ]
          ))


def calculate_age(birthday, release_date):
    """
    Calculate how many years an actor/actress had when a movie released.
    """
    if release_date['month'] > birthday['month'] or (release_date['month'] == birthday['month'] and release_date['day'] > birthday['day']):
        return str(release_date['year'] - birthday['year'])
    return str(release_date['year'] - 1 - birthday['year'])

class Person():
    """
    Abstraction for actors and actresses
    """
    def __init__(self, name, birthday, age_in_movie, id_number, picture):
        self.name = name
        self.birthday = Person.split_birthday(birthday) if birthday else None
        self.id = str(id_number)
        self.age = self.__calculate_age(self.birthday) if self.birthday else None
        self.age_in_movie = age_in_movie
        self.picture = picture if picture else None

    @staticmethod
    def split_birthday(birthday):
        return {'full': birthday,
                'year': int(birthday.split('-')[0]),
                'month': int(birthday.split('-')[1]),
                'day': int(birthday.split('-')[2])}

    def __calculate_age(self, birthday):
        if MONTH > birthday['month'] or (MONTH == birthday['month'] and DAY > birthday['day']):
            return str(YEAR - birthday['year'])
        return str(YEAR - 1 - birthday['year'])

    def data(self):
        return "{}: {}. Age: {}".format(self.id, self.name, self.age)

if __name__ == "__main__":
    search('How I Met Your Mother', 'serie')
