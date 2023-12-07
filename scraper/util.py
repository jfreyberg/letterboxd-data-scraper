import os
import random
from bs4 import BeautifulSoup as bs
from requests import get as rget
from time import sleep
from const import COOKIES, MIN_SLEEP, MAX_SLEEP



def getSleepTime(bonus=0):
    return random.randint(MIN_SLEEP + bonus, MAX_SLEEP + bonus)


def createPathIfNotExists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def getPageSoup(URL):
    bonus = 0
    while True:
        try:
            sleep(getSleepTime(bonus))
            res = rget(URL, cookies=COOKIES)
            soup = bs(res.text, 'html.parser')
            return soup
        except Exception as e:
            print(f'Error {e} getting page {URL}, trying again...')
            bonus += 5

def getNumberOfMoviesInCollection(collectionSoup):
    numberOfMovies = collectionSoup.find(class_='ui-block-heading').text
    numberOfMovies = ''.join(filter(lambda x: x.isdigit(), numberOfMovies))
    return numberOfMovies

def getNumberOfMoviesInYear(yearSoup):
    numberOfMovies = yearSoup.find(class_='ui-block-heading').text.split('films')[0]
    numberOfMovies = ''.join(filter(lambda x: x.isdigit(), numberOfMovies))
    return numberOfMovies

def getPosterContainers(yearSoup):
    posterList = yearSoup.find(class_='poster-list')
    posterContainers = posterList.find_all('div', class_='poster')
    return posterContainers

def getPartOfMovieInCollection(collectionSoup, movieSlug):
    collectionPosterContainers = getPosterContainers(collectionSoup)
    for ii, collectionPosterContainer in enumerate(collectionPosterContainers, 1):
        if collectionPosterContainer['data-film-slug'] == movieSlug:
            return ii


def getNumberOfMoviesInCollection(collectionSoup):
    numberOfMovies = collectionSoup.find(class_='ui-block-heading').text
    numberOfMovies = ''.join(filter(lambda x: x.isdigit(), numberOfMovies))
    if numberOfMovies == '':
        numberOfMovies = 0
    numberOfMovies = int(numberOfMovies)
    return numberOfMovies

def getNumberOfMoviesInYear(yearSoup):
    numberOfMovies = yearSoup.find(class_='ui-block-heading').text.split('films')[0]
    numberOfMovies = ''.join(filter(lambda x: x.isdigit(), numberOfMovies))
    return numberOfMovies

def getPosterContainers(yearSoup):
    posterList = yearSoup.find(class_='poster-list')
    posterContainers = posterList.find_all('div', class_='poster')
    return posterContainers

def getCollectionContainers(collectionsSoup):
    collectionsList = collectionsSoup.find(class_='list-grid')
    collectionsContainers = collectionsList.find_all('div', class_='-trilogy')
    return collectionsContainers

def getPartOfMovieInCollection(collectionSoup, movieSlug):
    collectionPosterContainers = getPosterContainers(collectionSoup)
    for ii, collectionPosterContainer in enumerate(collectionPosterContainers, 1):
        if collectionPosterContainer['data-film-slug'] == movieSlug:
            return ii
        
def getReleaseYear(movieSoup):
    return int(movieSoup.find('section', class_='film-header-lockup').find('small', class_='number').text)
