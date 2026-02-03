import random

random.seed()                                                             # Initialize the random number generator
print(random.getstate())                                                  # Returns the current internal state of the random number generator
random.setstate(random.getstate())                                        # Restores the internal state of the random number generator
print(random.getrandbits(8))                                              # Returns a number representing the random bits
print(random.randrange(0, 10))                                            # Returns a random number between the given range
print(random.randint(0, 10))                                              # Returns a random number between the given range
print(random.choice(['a', 'b', 'c']))                                     # Returns a random element from the given sequence
print(random.choices(['a', 'b', 'c', 'd', 'e', 'f']))                     # Returns a list with a random selection from the given sequence
print(random.shuffle(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']))      # Takes a sequence and returns the sequence in a random order
print(random.sample(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'], k=3))  # Returns a given sample of a sequence
print(random.random())                                                    # Returns a random float number between 0 and 1
print(random.uniform(10, 100))                                            # Returns a random float number between two given parameters
print(random.triangular())                                                # Returns a random float number between two given parameters, you can also set a mode parameter to specify the midpoint between the two other parameters
print(random.betavariate(1, 1))                                           # Returns a random float number between 0 and 1 based on the Beta distribution (used in statistics)
print(random.expovariate())                                               # Returns a random float number based on the Exponential distribution (used in statistics)
print(random.gammavariate(1, 1))                                          # Returns a random float number based on the Gamma distribution (used in statistics)
print(random.gauss())                                                     # Returns a random float number based on the Gaussian distribution (used in probability theories)
print(random.lognormvariate(1, 1))                                        # Returns a random float number based on a log-normal distribution (used in probability theories)
print(random.normalvariate())                                             # Returns a random float number based on the normal distribution (used in probability theories)
print(random.vonmisesvariate(1, 1))                                       # Returns a random float number based on the von Mises distribution (used in directional statistics)
print(random.paretovariate(1))                                            # Returns a random float number based on the Pareto distribution (used in probability theories)
print(random.weibullvariate(1, 1))                                        # Returns a random float number based on the Weibull distribution (used in statistics)