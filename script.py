# Note: Data comes from TMDb (themoviedb.org).

import json
import requests

API_KEY = 'f435496701f9d73f755d5bfb6cd880aa'
API_ENDPOINT = f'https://api.themoviedb.org/3/movie/now_playing?api_key={API_KEY}&language=en-US&page='

# Sends API GET request to fetch movie data
def requestMovies(pageNum):
    return requests.get(url = API_ENDPOINT + str(pageNum))

# Fetches movie data and deserializes JSON output
def getData(pageNum):
    response = requestMovies(pageNum)
    return json.loads(response.text)

# Filter to only include movies with at least 7.5 rating and 500 votes.
def filterMovies(movies):
    return [movie for movie in movies if movie['vote_count'] > 500 and movie['vote_average'] > 7.5]

# Get first page of data
data = getData(1)

# List of results containing information about each movie
results = data['results']
totalPages = data['total_pages']

# Repeat above steps for all pages
if totalPages > 1:
    for i in range(2, totalPages + 1):
        data = getData(i)
        results.extend(data['results'])

# Filter final list of movies
results = filterMovies(results)

print(results)