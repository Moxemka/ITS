from array import *
from random import randint
import time

#this function generates random array of 1000000 ints
def rand_arr_gen(): 
	_array = [0]*1000000
	for i in range(0, len(_array) - 1):
		_array[i] = randint(0, 999)
	return _array

#this function distributes the number of digits matching the given condition
def calc_hist(_data):
	hist = [0]*10
	for i in range(0, len(_data) - 1):
		pos = int(_data[i] / 100)
		if pos > 9: pos = 9
		hist[pos] += 1 


a = rand_arr_gen() #array with random numbers
time_data = array('d') #array with work time

#calculating time of work
for i in range(1, 101):
	start = time.time()
	calc_hist(a)
	end = time.time()
	time_data.append(end - start)


min = 9223372036854775807
max = -1
sum = 0

#time analysis: min, max, average
for i in range(0, len(time_data) - 1):
	if time_data[i] > max: 
		max = time_data[i]
	if time_data[i] < min: 
		min = time_data[i]
	sum += time_data[i]

print("max_value = ", max, "\n min_value = ", min, "\n average_value = ", sum / (len(time_data) - 1)) #printing results
	   



