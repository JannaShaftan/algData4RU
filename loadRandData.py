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
