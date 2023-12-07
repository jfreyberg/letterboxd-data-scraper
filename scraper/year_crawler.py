
import argparse
import pandas as pd
import numpy as np
from util import *
from const import MOVIES_PER_PAGE, collectionBaseURL, movieBaseURL, yearBaseURL

# get start year and end year from command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--start', type=int, help='The year to start crawling from', default = 1900, nargs='?')
parser.add_argument('--end', type=int, help='The year to end crawling at', default = -1, nargs='?')
parser.add_argument('--pages', type=int, help='The number of pages to crawl per year', default = 1, nargs='?')

args = parser.parse_args()
args.end = min(args.start + 9, 2022) if args.end == -1 else args.end

years = np.arange(args.start, args.end + 1)
pages = np.arange(1, args.pages + 1)

createPathIfNotExists('../data/years')
createPathIfNotExists('../data/total')

for page in pages:
    for year in years:
        # if csv file already exists, skip
        try:
            df = pd.read_csv(f'../data/years/{year}_{page}.csv')
            print(f'../data/years/{year}_{page}.csv already exists, skipping...')
            continue
        except:
            pass

        print(f'Getting data for {year} page {page}...')
        
        data = {'year': [], 'number': [], 'slug': [], 'partOfFranchise': [], 'inFranchise': [], 'franchiseLength': []} 

        yearURL = yearBaseURL + str(year) + '/page/' + str(page) + '/?esiAllowFilters=true'
        yearSoup = getPageSoup(yearURL)
        numberOfMoviesInYear = getNumberOfMoviesInYear(yearSoup)
        pd.DataFrame({'year': [year], 'numberOfMoviesInYear': [numberOfMoviesInYear]}).to_csv(f'../data/total/{year}.csv', index=False)
        posterContainers = getPosterContainers(yearSoup)
        for i, posterContainer in enumerate(posterContainers, 1):

            movieSlug = posterContainer['data-film-slug']
            movieURL = movieBaseURL.replace('<SLUG>', movieSlug)
            movieSoup = getPageSoup(movieURL)
            related = movieSoup.find(id='related')
            inFranchise = related != None
            number = i + (page - 1) * MOVIES_PER_PAGE
            partOfFranchise = 1
            franchiseLength = 0
            if inFranchise:
                collectionSlug = related.find('a')['href'].replace('/films/in/', '').replace('/by/release-earliest/size/large/', '')
                collectionURL = collectionBaseURL.replace('<SLUG>',collectionSlug)
                collectionSoup = getPageSoup(collectionURL)
                franchiseLength = getNumberOfMoviesInCollection(collectionSoup)
                partOfFranchise = getPartOfMovieInCollection(collectionSoup, movieSlug)
                if(franchiseLength == 0):
                    # case where the movie is the only one in the collection (e.g. because the others are unreleased)
                    partOfFranchise = 1
                    inFranchise = False

            data['year'].append(year)
            data['number'].append(number)
            data['partOfFranchise'].append(partOfFranchise)
            data['franchiseLength'].append(franchiseLength)
            data['inFranchise'].append(inFranchise)
            data['slug'].append(movieSlug)

        df = pd.DataFrame(data)
        df.to_csv(f'../data/years/{year}_{page}.csv', index=False)
