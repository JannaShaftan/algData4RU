from collections import defaultdict
import csv

def loadRandData(inf):
    allYearsTbl = defaultdict( lambda: defaultdict( dict )) # year -> city -> fld -> val
    reader = csv.DictReader(open(inf))
    for i,entry in enumerate(reader):
        # Year,City,Category,N
        year = int(entry['Year'])
        city = entry['City']
        cat = entry['Category']
        n = int(entry['N'])
        allYearsTbl[year][city][cat] = n
        
    return allYearsTbl

def findCitiesDict(allYearsTbl,baseYear):

    allYears = [y for y in allYearsTbl.keys()]
    oyears = {}
    for y in allYears:
        if y != baseYear:
            oyears[y] = []

    for bc in allYearsTbl[baseYear].keys():
        for oy in oyears.keys():
            if bc not in allYearsTbl[oy]:
                oyears[oy].append(bc)

    stats = [ (oy,len(oyears[oy])) for oy in oyears.keys() ]
    print 'findCitiesDict: %d vs: %s' % (baseYear,stats)

def findCitiesList(allYearsTbl,baseYear):

    allYears = [y for y in allYearsTbl.keys()]
    yearCities = {}
    oyears={}
    for y in allYears:
        if y != baseYear:
            oyears[y] = []
            yearCities[y] = allYearsTbl[y].keys()
    
    for bc in allYearsTbl[baseYear].keys():
        for oy in oyears.keys():
            if bc not in yearCities[oy]:
                oyears[oy].append(bc)

    stats = [ (oy,len(oyears[oy])) for oy in oyears.keys() ]
    print 'findCitiesList: %d vs: %s' % (baseYear,stats)

def findCitiesSet(allYearsTbl,baseYear):

    allYears = [y for y in allYearsTbl.keys()]
    baseSet = set(allYearsTbl[baseYear].keys())
    oset={}
    for y in allYears:
        if y != baseYear:
            oset[y] = set(allYearsTbl[y].keys())

    stats = [ (oy, len(baseSet - oset[oy])) for oy in oset.keys() ]
    print 'findCitiesSet: %d vs: %s' % (baseYear,stats)


import timeit

if __name__ == '__main__':

    inf = '/Data/sharedData/c4a_oakland/OAK_data/bs_anal/randCrimeData.csv'

    allYearsTbl = loadRandData(inf)

    ntrials = 5
    tl = timeit.timeit( 'findCitiesList(allYearsTbl,2013)', number = ntrials, setup="from __main__ import findCitiesList, allYearsTbl")
    print 'Using lists:',tl/ntrials,'sec'

    td = timeit.timeit( 'findCitiesDict(allYearsTbl,2013)', number =ntrials,setup="from __main__ import findCitiesDict, allYearsTbl")
    print 'Using dict:',td/ntrials,'sec'

    print 'Ratio list/dict', tl / td
    
    ts = timeit.timeit( 'findCitiesSet(allYearsTbl,2013)', number =ntrials,setup="from __main__ import findCitiesSet, allYearsTbl")
    print 'Using set:',ts/ntrials,'sec'

    print 'Ratio dict/set', td / ts

