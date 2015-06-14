import csv, math
from random import randint, random, shuffle
import matplotlib.pyplot as plt, numpy as np

# Markov Chain Monte Carlo method of solving the traveling salesman problem
# cities is a dict of city-coordinate pairs
# MAX_ITER is the number of iterations
# T is the Markov Chain Monte Carlo temperature
# Lower temperature results in a slower mixing time, and is more likely to
# result in a local optimum, but also requires fewer iterations
def MCMC(cities, MAX_ITER=10000, T=10):
	route = list(cities.items())
	best  = list(route)
	shuffle(route)

	curr_distance  = total_distance(route)
	best_distance  = total_distance(best) 
	
	for _ in xrange(MAX_ITER):
		new_route = create_new_route(route)
		new_distance   = total_distance(new_route)
		delta_distance = new_distance - curr_distance
		
		if (delta_distance < 0) or \
		(T > 0 and random() < math.exp(-1 * delta_distance / T)):
			route = new_route
			curr_distance = new_distance
		
		if curr_distance < best_distance:
			best = route
			best_distance = curr_distance

	return best

# route is a list of key-value tuples, e.g. ('City', [latitude, longitude])
def create_new_route(route):
	new_route = list(route)
	
	# generate indices for two random cities
	city_1, city_2 = (randint(0, len(route) - 1) for _ in xrange(2))
	
	# swap the cities
	new_route[city_1] = route[city_2]
	new_route[city_2] = route[city_1]
	
	return new_route

# route is a list of key-value tuples, e.g. ('City', [latitude, longitude])
def total_distance(route):
	dist = 0.0
	for i in xrange(len(route) - 1): # skip last element
		x = route[i]
		y = route[i+1]
		dist += distance(x, y)
	
	# we finish where we start, so add distance between last and first
	dist += distance(route[-1], route[0])
	return dist

# haversine distance between x and y
# x and y are kv tuples of the form ('City', [latitude, longitude])
def distance(x, y):
  # convert degrees to radians 
  lat_x, lon_x = map(math.radians, x[1])
  lat_y, lon_y = map(math.radians, y[1])

  # haversine of distance / radius
  h = (haversin(lat_y - lat_x) + math.cos(lat_x) * math.cos(lat_y)
  																									* haversin(lon_y - lon_x))
  r = 6371 # Radius of earth in kilometers
  d = 2.0 * r * math.asin(math.sqrt(h))
  return d

# the haversine function
def haversin(theta):
	return math.sin(theta / 2.0) ** 2

# Load the locations of the cities into memory
def get_cities(cities_csv_file="cities.csv"):
	with open(cities_csv_file, 'rU') as cities_csv:
		city_reader = csv.reader(cities_csv, delimiter = ',')
		next(city_reader) # skip first line (column headings)

		# we'll make a dict with city names as keys and coordinates as values
		# line[0] = city name, line[1] = latitude, line[2] = longitude
		cities = {line[0]:[float(line[1]), float(line[2])] for line in city_reader}
		return cities

def print_total_distance(route, verbose=False):
	dist = 0.0
	for i in xrange(len(route) - 1): # skip last element
		x = route[i]
		y = route[i+1]
		tmp = distance(x, y)
		if verbose:
			print "{} and {} are {} km apart.".format(x[0], y[0], int(tmp))
		dist += distance(x, y)

	# we finish where we start, so add distance between last and first
	x = route[-1]
	y = route[0]
	tmp = distance(x, y)
	if verbose:
		print "{} and {} are {} km apart.".format(x[0], y[0], int(tmp))
	dist += tmp

	print "The total distance is {} km.".format(int(dist))
	return dist

# This is MCMC with Simulated Annealing (i.e. T decreases over time)
def MCMC_SA(cities, MAX_ITER=10000, c=70):
	route = list(cities.items())
	best  = list(route)
	shuffle(route)

	curr_distance  = total_distance(route)
	best_distance  = total_distance(best) 
	
	for t in xrange(1, MAX_ITER+1):
		T = c / math.sqrt(t) 
		new_route = create_new_route(route)
		new_distance   = total_distance(new_route)
		delta_distance = new_distance - curr_distance
		
		if (delta_distance < 0) or \
		(T > 0 and random() < math.exp(-1 * delta_distance / T)):
			route = new_route
			curr_distance = new_distance
		
		if curr_distance < best_distance:
			best = route
			best_distance = curr_distance

	return best

def test():
	cities = get_cities()

	print "From the author:"
	print "The best result I've ever gotten is 17,632 km."
	print "If you're lucky, perhaps you can get a better result!"
	print
	
	print "Using MCMC with MAX_ITER = 10,000 and T = 0"
	route_1 = MCMC(cities, MAX_ITER=10000, T=0)
	print_total_distance(route_1)
	print

	print "Using MCMC with MAX_ITER = 10,000 and T = 1"
	route_2 = MCMC(cities, MAX_ITER=10000, T=1)
	print_total_distance(route_2)
	print

	print "Using MCMC with MAX_ITER = 10,000 and T = 10"
	route_3 = MCMC(cities, MAX_ITER=10000, T=10)
	print_total_distance(route_3)
	print

	print "Using MCMC with MAX_ITER = 10,000 and T = 100"
	route_4 = MCMC(cities, MAX_ITER=10000, T=100)
	print_total_distance(route_4)
	print

	print "Using MCMC with Simulated Annealing, MAX_ITER = 10,000 and c = 70"
	route_5 = MCMC_SA(cities, MAX_ITER=10000, c=70)
	print_total_distance(route_5)
	print

test()

# def MCMC_SA_MODIFIED(parks, MAX_ITER, c, successive_swaps):
# 	def create_new_route(route):
# 		def successive_indices():
# 			index_x = randint(0, len(route) - 1)
# 			index_y = (index_x + 1) if index_x == len(route) else 0
# 			return index_x, index_y

# 		def random_indices():
# 			index_x = randint(0, len(route) - 1)
# 			index_y = randint(0, len(route) - 1)
# 			return index_x, index_y
		
# 		new_route = list(route) # this list() call makes a copy of the list
# 		(index_x, index_y) = successive_indices() if successive_swaps else random_indices()
# 		swap(index_x, index_y, new_route)	
# 		return new_route

# 	intermediate_distance = [0.0 for _ in xrange(MAX_ITER)]
# 	best  = list(parks)
# 	route = list(parks)
# 	random.shuffle(route)
	
# 	for t in xrange(MAX_ITER):
# 		T = c / math.pow(t + 1, 0.5)
# 		new_route = create_new_route(route)
		
# 		# Some local variables to prevent recalculations
# 		new_distance   = total_distance(new_route)
# 		curr_distance  = total_distance(route)
# 		best_distance  = total_distance(best) 
		
# 		delta_distance = new_distance - curr_distance
		
# 		if (delta_distance < 0.0) or ((T > 0.0 and decision(delta_distance, T))):
# 			route = new_route
# 			curr_distance = new_distance
		
# 		if curr_distance < best_distance:
# 			best = route
# 			best_distance = curr_distance

# 		# We'll store the current distance after each iteration
# 		intermediate_distance[t] = curr_distance
# 	return best, best_distance, intermediate_distance

# def draw_plot(data, NUM_TRIALS, filename): 
# 	for i in xrange(NUM_TRIALS): 
# 		plt.plot(np.array(data[i]))
# 	plt.ylim(100, 700)
# 	plt.savefig(filename)
# 	plt.clf()

# def draw_plots(parks, NUM_TRIALS, MAX_ITER, successive_swaps, T, prefix):
# 	data = [[0.0]* MAX_ITER for i in xrange(NUM_TRIALS)]
# 	total = 0.0
# 	for i in xrange(NUM_TRIALS):
# 		_, best_distance, data[i] = MCMC(parks, MAX_ITER, T, successive_swaps)
# 		total += best_distance
# 		# print "Trial #{}: MCMC(parks, {}, {}, {}) = {}.".format(i, MAX_ITER, T, successive_swaps, best_distance)
# 	print " Mean for MCMC(parks, {}, {}, {}) = {}.".format(MAX_ITER, T, successive_swaps, total / NUM_TRIALS)
# 	print
# 	draw_plot(data, NUM_TRIALS, "{}T{}.png".format(prefix, int(T)))

# def draw_plots_SA(parks, NUM_TRIALS, MAX_ITER, successive_swaps, c, prefix):
# 	data = [[0.0]* MAX_ITER for i in xrange(NUM_TRIALS)]
# 	total = 0.0
# 	for i in xrange(NUM_TRIALS):
# 		_, best_distance, data[i] = MCMC_SA(parks, MAX_ITER, c, successive_swaps)
# 		total += best_distance
# 		# print "Trial #{}: MCMC_SA(parks, {}, {}, {}) = {}.".format(i, MAX_ITER, c, successive_swaps, best_distance)
# 	print " Mean for MCMC_SA(parks, {}, {}, {}) = {}.".format(MAX_ITER, c, successive_swaps, total / NUM_TRIALS)
# 	print
# 	draw_plot(data, NUM_TRIALS, "{}c{}.png".format(prefix, int(c)))

# def draw_plots_SA_MODIFIED(parks, NUM_TRIALS, MAX_ITER, successive_swaps, c, prefix):
# 	data = [[0.0]* MAX_ITER for i in xrange(NUM_TRIALS)]
# 	total = 0.0
# 	for i in xrange(NUM_TRIALS):
# 		_, best_distance, data[i] = MCMC_SA_MODIFIED(parks, MAX_ITER, c, successive_swaps)
# 		total += best_distance
# 		# print "Trial #{}: MCMC_SA_MODIFIED(parks, {}, {}, {}) = {}.".format(i, MAX_ITER, c, successive_swaps, best_distance)
# 	print " Mean for MCMC_SA_MODIFIED(parks, {}, {}, {}) = {}.".format(MAX_ITER, c, successive_swaps, total / NUM_TRIALS)
# 	print
# 	draw_plot(data, NUM_TRIALS, "{}c{}.png".format(prefix, int(c)))

# def draw_plots_SA_MODIFIED_AGAIN(parks, NUM_TRIALS, MAX_ITER, successive_swaps, c, prefix):
# 	data = [[0.0]* MAX_ITER for i in xrange(NUM_TRIALS)]
# 	total = 0.0
# 	for i in xrange(NUM_TRIALS):
# 		best, best_distance, data[i] = MCMC_SA_MODIFIED(parks, MAX_ITER, c, successive_swaps)
# 		total += best_distance
# 		# print "Trial #{}: MCMC_SA_MODIFIED(parks, {}, {}, {}) = {}.".format(i, MAX_ITER, c, successive_swaps, best_distance)
# 	print " Mean for MCMC_SA_MODIFIED(parks, {}, {}, {}) = {}.".format(MAX_ITER, c, successive_swaps, total / NUM_TRIALS)
# 	print

# def one_b(NUM_TRIALS=10, MAX_ITER=10000, successive_swaps=True):
# 	parks_dict = get_parks("p3_dataset/parks.csv") # K-V pairs => [('Park', [longitude, latitude])]
# 	parks = parks_dict.items()

# 	T = 0.0, 1.0, 10.0, 100.0
# 	for i in xrange(len(T)):
# 		draw_plots(parks, NUM_TRIALS, MAX_ITER, successive_swaps, T[i], "1B")

# # Successive_swaps is now false
# def one_d(NUM_TRIALS=10, MAX_ITER=10000, successive_swaps=False):
# 	parks_dict = get_parks("p3_dataset/parks.csv") # K-V pairs => [('Park', [longitude, latitude])]
# 	parks = parks_dict.items()

# 	T = 0.0, 1.0, 10.0, 100.0
# 	for i in xrange(len(T)):
# 		draw_plots(parks, NUM_TRIALS, MAX_ITER, successive_swaps, T[i], "1D")

# def one_d(NUM_TRIALS=10, MAX_ITER=10000, successive_swaps=False):
# 	parks_dict = get_parks("p3_dataset/parks.csv") # K-V pairs => [('Park', [longitude, latitude])]
# 	parks = parks_dict.items()

# 	T = 0.0, 1.0, 10.0, 100.0
# 	for i in xrange(len(T)):
# 		draw_plots(parks, NUM_TRIALS, MAX_ITER, successive_swaps, T[i], "1D")

# def two_a(NUM_TRIALS=10, MAX_ITER=10000, successive_swaps=False, c=70):
# 	parks_dict = get_parks("p3_dataset/parks.csv") # K-V pairs => [('Park', [longitude, latitude])]
# 	parks = parks_dict.items()
# 	draw_plots_SA(parks, NUM_TRIALS, MAX_ITER, successive_swaps, c, "2A")

# def two_c(NUM_TRIALS=10, MAX_ITER=10000, successive_swaps=False, c=70):
# 	parks_dict = get_parks("p3_dataset/parks.csv") # K-V pairs => [('Park', [longitude, latitude])]
# 	parks = parks_dict.items()
# 	draw_plots_SA_MODIFIED(parks, NUM_TRIALS, MAX_ITER, successive_swaps, c, "2C")

# def two_d(NUM_TRIALS=10, MAX_ITER=10000, successive_swaps=False, c=70)::
# 	parks_dict = get_parks("p3_dataset/parksContest.csv") # K-V pairs => [('Park', [longitude, latitude])]
# 	parks = parks_dict.items()
# 	draw_plots_SA_MODIFIED_AGAIN(parks, NUM_TRIALS, MAX_ITER, successive_swaps, c, "2D")



	
# one_b()
# one_d()
# two_a()
# two_c()