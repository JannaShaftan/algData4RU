## Preliminaries


* myDir = `/Users/rik/Writing/Consulting/EA/RocketU/curriculum`
* Socratic method
* Schedule
	* lectureA [20m] 
	* Practicum
		* Exercise 0,1,2,3 [10m]
		* Break [5m]
		* Discussion [10m]
		* Exercise 4 [15m]
	* lectureB [30m]


---
# AlgData4RocketU -Rik Belew - 17 Mar 2015


## Assumptions

2. Python is an excellent foundation. Get good at this language's:
	* features
		* [quickref](file:///Data/doc/Python/Python_2_6_quickRef.html)
	* [libraries](https://docs.python.org/2.7/) (eg, `datetime, os.path, json,   dbm, sqlite3, xml.*`)
	* [idioms](https://docs.python.org/2.7/howto/doanddont.html)
	* development tools (`unittest`)
	* debugging (`pdb, trace, timeit`)
	* runtime envt (`sys, gc`)

1. You may get/love **code** but get confused by **math**, or vice versa

1. You have (at least one) passion
	
1. Keep learning: You're in this for the long haul

	* Know what you don't know	
	* Invest wisely: choose what you want to learn


---

## Theoretic foundations

* Complexity
	* Time complexity: run time
	* Space complexity: required memory
	* (+) Time/space trade-offs remain relevant
	* (-) Complexity analysis typically cares about *worst-case* behavior
* Abstract data types
	* Data is defined by what you can do to/with it


![<fig:gareyJohnson>](/Users/rik/Writing/Consulting/EA/RocketU/curriculum/figs/gareyJohnson-3.jpg "<fig:gareyJohnson>")

---

## Numbers

* Integers are infinite but countable
* `int` give >= 32 bits
* `long` automagically provides as many bits as required!
* Real numbers are *uncountably* infinite
	* Exponent, mantissa represented separately
	* Be careful about tests 
		* eg, `r == 0.`
		* eg, `geoLatitude1 == geoLatitude2`
* Computers are just this stupid: you need to tell them *everything*!

![<fig:Floating point>](/Users/rik/Writing/Consulting/EA/RocketU/curriculum/figs/floatingPoint_PattPatel.gif "<fig:Floating point>")

---

## Lists
* `l = []`
	* supports `append(), insert(), extend()`, indexed access, ...
	* heterogeneous element types

* [Performance](https://wiki.python.org/moin/TimeComplexity): "Amortized worst-case" performance ~ constant 

* CPython implementation

		typedef struct {
		    PyObject_VAR_HEAD
		    PyObject **ob_item;
		    Py_ssize_t allocated;
		} PyListObject;
		
	* NB: over-allocated!
	
* space-inefficient for homogeneous data

* shallow vs. deep copies [[PyDoc]](https://docs.python.org/2/library/copy.html) "A shallow copy constructs a new compound object and then (to the extent possible) inserts references into it to the objects found in the original. A deep copy constructs a new compound object and then, recursively, inserts copies into it of the objects found in the original."
    
---

## Arrays

* homogeneous data elements allows exploitation of "address arithmetic"

* `array.array(typecode[, initializer])`
	* Simple wrapper around C data types

* `numpy.array(object)`
	* statistics, linear algebra, ...!
	* [SciPy](http://www.scipy.org/), [Pandas](http://pandas.pydata.org/), [scikit-learn](http://scikit-learn.org/), ...
	

---

## Hashing (dictionaries)

* *Hashing function*: mapping from large sets of keys to finite set of "buckets"
	* collisions may occur, but are to be avoided
	* keys cannot be mutable
* [space complexity considerations](http://stackoverflow.com/questions/2747511/why-do-dicts-of-defaultdictints-use-so-much-memory-and-other-simple-python)

* `collections.defaultdict(factoryType)` !
	* "This technique is simpler and faster than an equivalent technique using 		`dict.setdefault()`" [PythonDoc]
	* `int`, `list`, `dict`, `set` factories
		
	* multi-level with recursive factory function!

* "multidict": key -> list of values


---

## PRACTICUM: Crime ranks

### test data file

	`less randCrimeData.csv`
  
		Year,City,Category,N
		2004,Dus_NORA,pop,11092
		2004,Dus_NORA,aa,33
		2004,Dus_NORA,arson,2
		2004,Dus_NORA,burglary,116
		2004,Dus_NORA,motorTheft,40
		2004,Dus_NORA,pcrime,714
		2004,Dus_NORA,robbery,8
		2004,Henria_NEBRAA,pop,118705
		2004,Henria_NEBRAA,aa,254
		2004,Henria_NEBRAA,arson,72
		...

	`wc randCrimeData.csv`

		  214796  214796 5963460 randCrimeData.csv

---

### `loadRandDataTbl(inf)`

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

---

###  0. `basicStats(l)`

Returns avg and [standard deviation](http://en.wikipedia.org/wiki/Standard_deviation) of elements in list l


---

###  1. `findCities(allYearsTbl,baseYear)`

Write a function that contrasts the cities in `allYearsTbl[baseYear]` with those in all other years, and returns a list of the *number of cities* that are in `allYearsTbl[baseYear]` but are *missing* in `allYearsTbl[otherYear]`, in the format: `[ (otherYear, nmissing) ]`.  

For example, for `baseYear=2013` it should return `[(2009, 1300), (2004, 6538), (2012, 667)]`

Use `timeit` to evaluate the performance of your routine.
	
---


###  2. `filterSmallCities(allYearTbl,minPopsize,baseYear=None)`

Return identically shaped `allYearTbl`, but only for cities whose population in `baseYear` was at least `minPopsize`.  If `baseYear` not given, use *most recent year* as `baseYear`.

NB: if a city's population is above threshold in `baseYear`, include its data for *all* years.

---

###  3. `rptPop(allYearTbl,baseYear,outf)`

For all cities in `allYearsTbl[baseYear]`, gather populations across all  other years, and report in CSV formatted outf with header line similar to `City,2013,2012,2009,2004`.  

NB: Report pop=0 for any years for which a city is not included in a year's data.

---

###  4. `rptNearComps(allYearTbl,targetCity,baseYear,outf)`

You live in city `targetCity` and are curious how other cities are dealing with their crime.  For example, what cities were experiencing similar levels of `AA` crime in 2009, but have improved in 2013? 

For each crime category, report those cities with nearly the same *normalized rank level* of crime in `baseYear` as our city, and report what their rank was in all other years.  

Define *normalized rank level* as follows: first divide the number of crimes of a type by the city's population.  Then *sort* all cities from least to most.  A city's normalized rank level is its position in this sorted list.  By "nearly the same," mean with rank within 10 of `targetCity`.

Produce a CSV report like the following:

![<fig:nearCompEg>](/Users/rik/Writing/Consulting/EA/RocketU/curriculum/figs/nearCompsExample.jpg "<fig:fig:nearCompEg>") 

---

## Trees

* more than one pointer from each data node gives lots of alternatives

* binary search is efficient

* **Graph**: nodes + edges

* **Tree**: graph with identified "root" 

* **Traversal**: Beginning at root, visit connected nodes in a graph

---

## DFS

		def dfs(graph, start, visited=None):
		    if visited is None:
		        visited = set()
		    visited.add(start)
		    for next in graph[start] - visited:
		        dfs(graph, next, visited)
		    return visited
---

## BFS

		def bfs(graph, start):
		    visited, queue = set(), [start]
		    while queue:
		        vertex = queue.pop(0)
		        if vertex not in visited:
		            visited.add(vertex)
		            queue.extend(graph[vertex] - visited)
		    return visited

---

## Traversal viz

* [Steven Halim National University of Singapore](http://visualgo.net/dfsbfs.html)

* [David Galles, USF](http://www.cs.usfca.edu/~galles/visualization/Algorithms.html)

---

## Heaps

* python `heapq`

* Heaps are arrays for which `a[k] <= a[2*k+1]` and `a[k] <= a[2*k+2]` for all `k`, counting elements from 0.

* great for 
	* scheduling events into the future
	* Big out-of-memory merge-sorts

---

## Other topics

* Graph theory

* special graphs
	* bipartite

* profiling
	* time
	* space

* Python libraries

* Databases

* Geographic data
