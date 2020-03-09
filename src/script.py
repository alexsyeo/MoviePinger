# Note: Data comes from TMDb (themoviedb.org).

import json
import requests
import smtplib, ssl

from getpass import getpass

API_KEY = 'f435496701f9d73f755d5bfb6cd880aa'
API_ENDPOINT = f'https://api.themoviedb.org/3/movie/upcoming?api_key={API_KEY}&language=en-US&region=US&page='
SENDER_EMAIL = input("Type in sender email address and press enter: ")
RECEIVER_EMAIL = input("Type in receiver email address and press enter: ")

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
    emailMessage = ''
    for movie in movieInfo:
        emailMessage += f'Title: {movie["title"]}\nPopularity: {movie["popularity"]}\nRelease Date: {movie["release_date"]}\nOverview: {movie["overview"]}\n\n\n'
    return emailMessage.encode("utf-8")


# Send email with movie information
# Some of the below code taken from https://realpython.com/python-send-email/#starting-a-secure-smtp-connection
def sendMovieInfoEmail(movieInfo):
    port = 465
    smtp_server = "smtp.gmail.com"

    print("Enter password of sender email address.")
    password = getpass()

    # Create the content of the email
    message = constructEmailMessage(movieInfo)

    # Create secure SSL context
    context = ssl.create_default_context()

    # Send the email
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(SENDER_EMAIL, password)
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
            print('before first send')
            sendMovieInfoEmail(moviesToSend)

            print('After send')
            
            # Add movies to files
            storedResults.extend(moviesToSend)
            json.dump(storedResults, jsonfile)
            print('After dump')

    except:
        # Send email with movie information
        print('before second send')
        sendMovieInfoEmail(results)
        
        # Add movies to files
        json.dump(results, jsonfile)