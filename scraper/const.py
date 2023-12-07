# cookies are necessary to filter out TV, shorts, docs, and unreleased films
COOKIES = {'filmFilter': 'hide-tv%20hide-shorts%20hide-docs%20hide-unreleased'}
MOVIES_PER_PAGE = 72
MIN_SLEEP = 5
MAX_SLEEP = 10
collectionsBaseURL = 'https://letterboxd.com/collections/popular/page/'
collectionBaseURL = 'https://letterboxd.com/films/ajax/in/<SLUG>/by/release-earliest/?esiAllowFilters=true'
movieBaseURL = 'https://letterboxd.com/film/<SLUG>'
yearBaseURL = 'https://letterboxd.com/films/ajax/popular/year/'
