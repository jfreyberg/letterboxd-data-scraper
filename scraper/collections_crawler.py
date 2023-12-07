from requests import get as rget
from time import sleep
from bs4 import BeautifulSoup as bs
import pandas as pd
from util import *
from const import collectionsBaseURL, collectionBaseURL, movieBaseURL

pages = list(range(1, 50))
createPathIfNotExists('..data/collections')


for page in pages:
    try:
        df = pd.read_csv(f'..data/collections/{page}.csv')
        print(f'..data/collections/{page}.csv already exists, skipping...')
        continue
    except:
        pass

    print(f'Getting data for page {page}...')
    
    data = {'title':[], 'part': [], 'slug': [], 'franchise': [], 'franchiseLength': [], 'rating': [], 'year': []}
    

    collectionsSoup = getPageSoup(collectionsBaseURL + str(page))
    collectionContainers = getCollectionContainers(collectionsSoup)

    broken = []
    for i, collectionContainer in enumerate(collectionContainers, 1):
        collectionTitle = collectionContainer.find('h3').find('a').text
        print(f'Getting data for {collectionTitle} ({i}/{len(collectionContainers)})')
        collectionSlug = collectionContainer.find('a')['href'].replace('/films/in/', '').replace('/by/release-earliest/size/large/', '')
        collectionURL = collectionBaseURL.replace('<SLUG>', collectionSlug)
        collectionSoup = getPageSoup(collectionURL)
        collectionLength = getNumberOfMoviesInCollection(collectionSoup)
        if(collectionLength < 2):
            continue

        for partOfFranchise, posterContainer in enumerate(collectionSoup.find_all('li', class_='poster-container'), 1):
            try:
                movieRating = posterContainer['data-average-rating']
            except:
                broken.append(collectionTitle)
                break
            movieSlug = posterContainer.find('div')['data-film-slug']
            movieURL = movieBaseURL.replace('<SLUG>', movieSlug)
            movieSoup = getPageSoup(movieURL)
            movieYear = getReleaseYear(movieSoup)
            movieTitle = posterContainer.find('div').find('img')['alt']

            data['year'].append(movieYear)
            data['title'].append(movieTitle)
            data['part'].append(partOfFranchise)
            data['slug'].append(movieSlug)
            data['franchise'].append(collectionTitle)
            data['franchiseLength'].append(collectionLength)
            data['rating'].append(movieRating)

    df = pd.DataFrame(data)
    df = df[~df['franchise'].isin(broken)]


    df.to_csv(f'../data/collections/{page}.csv', index=False)
