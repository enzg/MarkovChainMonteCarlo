# MarkovChainMonteCarlo
An example of the Markov chain Monte Carlo method

***

This is a python example of using the Markov chain Monte Carlo (MCMC) method to solve the travelling salesman problem. I learned MCMC in Stanford's CS 168 (taught by Profs. Greg Valiant and Tim Roughgarden.) 

## Files

`cities.csv` is a csv file of the fifty most-populated American cities and their geographic coordinates. I wrote it by hand from [Wikipedia](https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population) - if I made any mistakes when entering the data, please let me know!

`mcmc.py` contains the code for the MCMC method. To use it, simply run it in your favorite Python interpreter; it will use MCMC to quickly find a short route that traverses the fifty most-populated American cities.
