# Note: Data comes from TMDb (themoviedb.org).

import datetime
import json
import requests
import smtplib, ssl
import sys

API_KEY = 'f435496701f9d73f755d5bfb6cd880aa'
API_ENDPOINT = f'https://api.themoviedb.org/3/movie/upcoming?api_key={API_KEY}&language=en-US&region=US&page='

SENDER_EMAIL = sys.argv[1]
RECEIVER_EMAIL = sys.argv[2]
SENDER_PASSWORD = sys.argv[3]

# Returns the current date and time
def getNow():
    return datetime.datetime.now().strftime("%c")

# Sends API GET request to fetch movie data
def requestMovies(pageNum):
    return requests.get(url = API_ENDPOINT + str(pageNum))


# Fetches movie data and deserializes JSON output
def getData(pageNum):
    response = requestMovies(pageNum)
    return json.loads(response.text)


# Filter to only include movies with at least 15.0 popularity
def filterMovies(movies):
    return [movie for movie in movies if movie['popularity'] > 15.0]


# Takes in movie info as JSON data and converts to email message string (utf-8 encoded)
def constructEmailMessage(movieInfo):
    emailSubject = f'Subject: [{getNow()}] Upcoming movies from MoviePinger'
    emailMessage = ''
    for movie in movieInfo:
        emailMessage += f'Title: {movie["title"]}\nPopularity: {movie["popularity"]}\nRelease Date: {movie["release_date"]}\nOverview: {movie["overview"]}\n\n\n'
    return (emailSubject + '\n\n' + emailMessage).encode("utf-8")


# Send email with movie information
# Some of the below code taken from https://realpython.com/python-send-email/#starting-a-secure-smtp-connection
def sendMovieInfoEmail(movieInfo):
    port = 465
    smtp_server = "smtp.gmail.com"

    # Create the content of the email
    message = constructEmailMessage(movieInfo)

    # Create secure SSL context
    context = ssl.create_default_context()

    # Send the email
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message)


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

# Check local file to see if the movies have already been pinged before
# NOTE: Currently assumes that the file exists
with open('data/data.json', 'r+') as jsonfile:
    try:
        storedResults = json.load(jsonfile)
        moviesToSend = []
        for movie in results:
            if movie not in storedResults:
                moviesToSend.append(movie)
        if moviesToSend:
            # Send email with movie information
            sendMovieInfoEmail(moviesToSend)

            # Add movies to files
            storedResults.extend(moviesToSend)
            json.dump(storedResults, jsonfile)
    except:
        # Send email with movie information
        sendMovieInfoEmail(results)
        
        # Add movies to files
        json.dump(results, jsonfile)