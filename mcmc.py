import csv, math, random, matplotlib.pyplot as plt, numpy as np
from collections import OrderedDict

def get_parks(path):
	with open(path, 'rU') as parks_csv:
		parks_reader = csv.reader(parks_csv, delimiter = ',')
		parks = OrderedDict()
		for line in parks_reader:
			if line[0] != "Name":
				parks[line[0]] = [float(line[1]), float(line[2])]
		return parks

def distance(x, y): # x and y are lists, e.g. x = [longitude, latitude]
	return math.sqrt(((x[0] - y[0]) ** 2) + ((x[1] - y[1]) ** 2))

# parks is a list of dict key-value pairs, e.g. [('Park', [longitude, latitude])]
def total_distance(parks):
	dist = 0.0
	for index, park_element in enumerate(parks, start=1):
		index_x = index - 1
		index_y = index if index != len(parks) else 0
		dist += distance(parks[index_x][1], parks[index_y][1])
	return dist

def print_total_distance(parks):
	dist = 0.0
	for index, park_element in enumerate(parks, start=1):
		index_x = index - 1
		index_y = index if index != len(parks) else 0
		temp = distance(parks[index_x][1], parks[index_y][1])
		print "{}. The distance from {} to {} is {}".format(index, parks[index_x][0], parks[index_y][0], temp)
		dist += temp
	print "The total distance is {}".format(dist)
	print
	return dist

def swap(index_x, index_y, parks):
	parks[index_x], parks[index_y] = parks[index_y], parks[index_x]

def decision(delta_distance, T):
	exponent = -1 * delta_distance / T
	return random.random() < math.exp(exponent)

def sanity_check():
	parks_dict = get_parks("p3_dataset/parks.csv") # K-V pairs => [('Park', [longitude, latitude])]
	parks = parks_dict.items()

	if distance(parks[0][1], parks[1][1]) != distance(parks[1][1], parks[0][1]):
		raise RuntimeError
	
	dist = print_total_distance(parks)
	if dist != total_distance(parks):
		raise RuntimeError
	
	print "The first thre elements are {}, {}, {}.".format(parks[0][0], parks[1][0], parks[2][0])
	swap(0, 1, parks)
	print "After the first two are swapped, they are {}, {}, {}.".format(parks[0][0], parks[1][0], parks[2][0])
	print

	print "This should be true with 100% probability: {}.".format(decision(0, 1))
	print "This should be true with   0% probability: {}.".format(decision(10000, 0.00001))
	print

	print "This should be true with  50% probability: {}.".format(decision(-1 * math.log(0.5), 1))
	print "This should be true with  50% probability: {}.".format(decision(-1 * math.log(0.5), 1))
	print "This should be true with  50% probability: {}.".format(decision(-1 * math.log(0.5), 1))
	print "This should be true with  50% probability: {}.".format(decision(-1 * math.log(0.5), 1))
	print "This should be true with  50% probability: {}.".format(decision(-1 * math.log(0.5), 1))
	print "This should be true with  50% probability: {}.".format(decision(-1 * math.log(0.5), 1))

def MCMC(parks, MAX_ITER, T, successive_swaps):
	# parks is a list of dict key-value pairs
	# e.g. [('Park', [longitude, latitude])]
	# successive_swaps is true in 1b, and false in 1d

	def create_new_route(route):
		def successive_indices():
			index_x = random.randint(0, len(route) - 1)
			index_y = (index_x + 1) if index_x == len(route) else 0
			return index_x, index_y

		def random_indices():
			index_x = random.randint(0, len(route) - 1)
			index_y = random.randint(0, len(route) - 1)
			return index_x, index_y
		
		new_route = list(route) # this list() call makes a copy of the list
		(i, j) = successive_indices() if successive_swaps else random_indices()
		swap(i, j, new_route)	
		return new_route

	intermediate_distance = [0.0 for _ in xrange(MAX_ITER)]
	best  = list(parks)
	route = list(parks)
	random.shuffle(route)
	
	for i in xrange(MAX_ITER):
		new_route = create_new_route(route)
		
		# Some local variables to prevent recalculations
		new_distance   = total_distance(new_route)
		curr_distance  = total_distance(route)
		best_distance  = total_distance(best) 
		
		delta_distance = new_distance - curr_distance
		
		if (delta_distance < 0) or ((T > 0 and decision(delta_distance, T))):
			route = new_route
			curr_distance = new_distance
		
		if curr_distance < best_distance:
			best = route
			best_distance = curr_distance

		# We'll store the current distance after each iteration
		# to use when plotting
		intermediate_distance[i] = curr_distance
	return best, best_distance, intermediate_distance

def MCMC_SA(parks, MAX_ITER, c, successive_swaps):
	def create_new_route(route):
		def successive_indices():
			index_x = random.randint(0, len(route) - 1)
			index_y = (index_x + 1) if index_x == len(route) else 0
			return index_x, index_y

		def random_indices():
			index_x = random.randint(0, len(route) - 1)
			index_y = random.randint(0, len(route) - 1)
			return index_x, index_y
		
		new_route = list(route) # this list() call makes a copy of the list
		(i, j) = successive_indices() if successive_swaps else random_indices()
		swap(i, j, new_route)	
		return new_route

	intermediate_distance = [0.0 for _ in xrange(MAX_ITER)]
	best  = list(parks)
	route = list(parks)
	random.shuffle(route)
	
	for t in xrange(MAX_ITER):
		T = c / math.sqrt(t + 1)
		new_route = create_new_route(route)
		
		# Some local variables to prevent recalculations
		new_distance   = total_distance(new_route)
		curr_distance  = total_distance(route)
		best_distance  = total_distance(best) 
		
		delta_distance = new_distance - curr_distance
		
		if (delta_distance < 0) or ((T > 0 and decision(delta_distance, T))):
			route = new_route
			curr_distance = new_distance
		
		if curr_distance < best_distance:
			best = route
			best_distance = curr_distance

		# We'll store the current distance after each iteration
		intermediate_distance[t] = curr_distance
	return best, best_distance, intermediate_distance

def MCMC_SA_MODIFIED(parks, MAX_ITER, c, successive_swaps):
	def create_new_route(route):
		def successive_indices():
			index_x = random.randint(0, len(route) - 1)
			index_y = (index_x + 1) if index_x == len(route) else 0
			return index_x, index_y

		def random_indices():
			index_x = random.randint(0, len(route) - 1)
			index_y = random.randint(0, len(route) - 1)
			return index_x, index_y
		
		new_route = list(route) # this list() call makes a copy of the list
		(index_x, index_y) = successive_indices() if successive_swaps else random_indices()
		swap(index_x, index_y, new_route)	
		return new_route

	intermediate_distance = [0.0 for _ in xrange(MAX_ITER)]
	best  = list(parks)
	route = list(parks)
	random.shuffle(route)
	
	for t in xrange(MAX_ITER):
		T = c / math.pow(t + 1, 0.5)
		new_route = create_new_route(route)
		
		# Some local variables to prevent recalculations
		new_distance   = total_distance(new_route)
		curr_distance  = total_distance(route)
		best_distance  = total_distance(best) 
		
		delta_distance = new_distance - curr_distance
		
		if (delta_distance < 0.0) or ((T > 0.0 and decision(delta_distance, T))):
			route = new_route
			curr_distance = new_distance
		
		if curr_distance < best_distance:
			best = route
			best_distance = curr_distance

		# We'll store the current distance after each iteration
		intermediate_distance[t] = curr_distance
	return best, best_distance, intermediate_distance

def draw_plot(data, NUM_TRIALS, filename): 
	for i in xrange(NUM_TRIALS): 
		plt.plot(np.array(data[i]))
	plt.ylim(100, 700)
	plt.savefig(filename)
	plt.clf()

def draw_plots(parks, NUM_TRIALS, MAX_ITER, successive_swaps, T, prefix):
	data = [[0.0]* MAX_ITER for i in xrange(NUM_TRIALS)]
	total = 0.0
	for i in xrange(NUM_TRIALS):
		_, best_distance, data[i] = MCMC(parks, MAX_ITER, T, successive_swaps)
		total += best_distance
		# print "Trial #{}: MCMC(parks, {}, {}, {}) = {}.".format(i, MAX_ITER, T, successive_swaps, best_distance)
	print " Mean for MCMC(parks, {}, {}, {}) = {}.".format(MAX_ITER, T, successive_swaps, total / NUM_TRIALS)
	print
	draw_plot(data, NUM_TRIALS, "{}T{}.png".format(prefix, int(T)))

def draw_plots_SA(parks, NUM_TRIALS, MAX_ITER, successive_swaps, c, prefix):
	data = [[0.0]* MAX_ITER for i in xrange(NUM_TRIALS)]
	total = 0.0
	for i in xrange(NUM_TRIALS):
		_, best_distance, data[i] = MCMC_SA(parks, MAX_ITER, c, successive_swaps)
		total += best_distance
		# print "Trial #{}: MCMC_SA(parks, {}, {}, {}) = {}.".format(i, MAX_ITER, c, successive_swaps, best_distance)
	print " Mean for MCMC_SA(parks, {}, {}, {}) = {}.".format(MAX_ITER, c, successive_swaps, total / NUM_TRIALS)
	print
	draw_plot(data, NUM_TRIALS, "{}c{}.png".format(prefix, int(c)))

def draw_plots_SA_MODIFIED(parks, NUM_TRIALS, MAX_ITER, successive_swaps, c, prefix):
	data = [[0.0]* MAX_ITER for i in xrange(NUM_TRIALS)]
	total = 0.0
	for i in xrange(NUM_TRIALS):
		_, best_distance, data[i] = MCMC_SA_MODIFIED(parks, MAX_ITER, c, successive_swaps)
		total += best_distance
		# print "Trial #{}: MCMC_SA_MODIFIED(parks, {}, {}, {}) = {}.".format(i, MAX_ITER, c, successive_swaps, best_distance)
	print " Mean for MCMC_SA_MODIFIED(parks, {}, {}, {}) = {}.".format(MAX_ITER, c, successive_swaps, total / NUM_TRIALS)
	print
	draw_plot(data, NUM_TRIALS, "{}c{}.png".format(prefix, int(c)))

def draw_plots_SA_MODIFIED_AGAIN(parks, NUM_TRIALS, MAX_ITER, successive_swaps, c, prefix):
	data = [[0.0]* MAX_ITER for i in xrange(NUM_TRIALS)]
	total = 0.0
	for i in xrange(NUM_TRIALS):
		best, best_distance, data[i] = MCMC_SA_MODIFIED(parks, MAX_ITER, c, successive_swaps)
		total += best_distance
		# print "Trial #{}: MCMC_SA_MODIFIED(parks, {}, {}, {}) = {}.".format(i, MAX_ITER, c, successive_swaps, best_distance)
	print " Mean for MCMC_SA_MODIFIED(parks, {}, {}, {}) = {}.".format(MAX_ITER, c, successive_swaps, total / NUM_TRIALS)
	print

def one_b(NUM_TRIALS=10, MAX_ITER=10000, successive_swaps=True):
	parks_dict = get_parks("p3_dataset/parks.csv") # K-V pairs => [('Park', [longitude, latitude])]
	parks = parks_dict.items()

	T = 0.0, 1.0, 10.0, 100.0
	for i in xrange(len(T)):
		draw_plots(parks, NUM_TRIALS, MAX_ITER, successive_swaps, T[i], "1B")

# Successive_swaps is now false
def one_d(NUM_TRIALS=10, MAX_ITER=10000, successive_swaps=False):
	parks_dict = get_parks("p3_dataset/parks.csv") # K-V pairs => [('Park', [longitude, latitude])]
	parks = parks_dict.items()

	T = 0.0, 1.0, 10.0, 100.0
	for i in xrange(len(T)):
		draw_plots(parks, NUM_TRIALS, MAX_ITER, successive_swaps, T[i], "1D")

def one_d(NUM_TRIALS=10, MAX_ITER=10000, successive_swaps=False):
	parks_dict = get_parks("p3_dataset/parks.csv") # K-V pairs => [('Park', [longitude, latitude])]
	parks = parks_dict.items()

	T = 0.0, 1.0, 10.0, 100.0
	for i in xrange(len(T)):
		draw_plots(parks, NUM_TRIALS, MAX_ITER, successive_swaps, T[i], "1D")

def two_a(NUM_TRIALS=10, MAX_ITER=10000, successive_swaps=False, c=70):
	parks_dict = get_parks("p3_dataset/parks.csv") # K-V pairs => [('Park', [longitude, latitude])]
	parks = parks_dict.items()
	draw_plots_SA(parks, NUM_TRIALS, MAX_ITER, successive_swaps, c, "2A")

def two_c(NUM_TRIALS=10, MAX_ITER=10000, successive_swaps=False, c=70):
	parks_dict = get_parks("p3_dataset/parks.csv") # K-V pairs => [('Park', [longitude, latitude])]
	parks = parks_dict.items()
	draw_plots_SA_MODIFIED(parks, NUM_TRIALS, MAX_ITER, successive_swaps, c, "2C")

def two_d(NUM_TRIALS=10, MAX_ITER=10000, successive_swaps=False, c=70)::
	parks_dict = get_parks("p3_dataset/parksContest.csv") # K-V pairs => [('Park', [longitude, latitude])]
	parks = parks_dict.items()
	draw_plots_SA_MODIFIED_AGAIN(parks, NUM_TRIALS, MAX_ITER, successive_swaps, c, "2D")



	
# one_b()
# one_d()
# two_a()
# two_c()