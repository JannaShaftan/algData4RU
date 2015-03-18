from collections import defaultdict
import csv
import math

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

def basicStats(l):
    "Returns avg and stdev"
    if len(l) == 0:
        return(0.,0.)

    sum = 0
    for n in l:
        sum += n
    avg = float(sum) / len(l)

    sumDiffSq = 0.
    for n in l:
        sumDiffSq += (n-avg)*(n-avg)

    stdev = math.sqrt(sumDiffSq) / float(len(l))
    return (avg,stdev)

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


def rptPop(allYearTbl,baseYear,outf):
    '''For all cities in allYearsTbl[baseYear], gather populations across all  other years
        NB: Report pop=0 for any years for which a city is not included in a years data.
    '''

    oyears = [y for y in allYearTbl.keys() if y != baseYear]
    oyears.sort()
    
    popTbl = {} # city -> yr -> pop
    nzero = 0
    for city in allYearTbl[baseYear]:
        pop = allYearTbl[baseYear][city]['pop']
        if pop < 1e5:
            continue
        popTbl[city] = {baseYear: pop}
        for oy in oyears:
            if city in allYearTbl[oy]:
                popTbl[city][oy] = allYearTbl[oy][city]['pop']
            else:
                popTbl[city][oy] = 0
                nzero += 1
    
    print 'rptPop: NCities=%d NZeroYr=%d' % (len(popTbl),nzero)
    allCities = popTbl.keys()
    allCities.sort(key=lambda c: popTbl[c][2013], reverse=True)
    outs = open(outf,'w')
    hdrLine = 'City'
    hdrLine += (',%d' % baseYear)
    for oy in oyears:
        hdrLine += (',%d' % oy)
    outs.write(hdrLine+'\n')
    
    for city in allCities:
        outs.write('%s' % (city))
        for y in [baseYear] + oyears:
            outs.write(',%d' % popTbl[city][y])
        outs.write('\n')
    outs.close()

def filterSmallCities(allYearTbl,minPopsize,baseYear=None):
    '''Return identically shaped `allYearTbl`, but only for cities 
        whose population in `baseYear` was at least `minPopsize`.  
        If `baseYear` not given, use *most recent year* as `baseYear`.
        NB: if a citys population is above threshold in `baseYear`, include its data for *all* years.
    '''

    if not baseYear:
        allYears = allYearTbl.keys()
        baseYear = max(allYears)
    
    bigCities = {}
    for cityState in allYearTbl[baseYear].keys():
        if allYearTbl[baseYear][cityState]['pop'] >= minPopsize:
            bigCities[cityState] = 1
            
    newTbl = {} # year -> city -> crimeType -> freq
    for year in allYearTbl.keys():
        newYearTbl = {}
        for cityState in allYearTbl[year].keys():
            if cityState in bigCities:
                newYearTbl[cityState] = allYearTbl[year][cityState].copy()
                
        # Add any cities in bigCities that aren't in allYearTbl[year] with just their pop
        for bc in bigCities:
            if bc not in newYearTbl:
                newYearTbl[cityState] = {'pop': allYearTbl[baseYear][bc]['pop'] }
        newTbl[year] = newYearTbl
             
    return newTbl

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

