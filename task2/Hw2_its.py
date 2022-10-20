from array import *
import math

#this function is used for print an array 
def print_normaly(_str):
    a = ""
    for i in range(0, len(_str)):
        a += _str[i] + " "
    print(a)

#this function creates and prints triangles by defined formula 
def draw_triangle(a):
    general_string = [" "] * (a * 2 + 1)
    general_string[a] = "*"
    print_normaly(general_string)

    for i in range(1, a + 1):
            general_string[a + i] = "*"
            general_string[a - i] = "*"
            print_normaly(general_string)
    
#this function calculates distance between 2 vectors 
def hist_distance(hist1, hist2):
    if len(hist1) - len(hist2) != 0:
        print("2 вектора должны быть одинаковы по длине")
        return
    squared_sum = 0.0
    for i in range(0, len(hist1)): squared_sum += (hist1[i] - hist2[i]) * (hist1[i] - hist2[i])
    return math.sqrt(squared_sum)

#this function creates a file of hist with defined name
def serialisaition(hist1, name):
      f = open(name + '.txt', 'w')
      for i in range(0, len(hist1)):
          f.write(str(hist1[i]) + '\n')
      f.close()
      print('file created with name = ',name,'.txt')

#this function reads a file of hist with defined name
def de_serialisaition(name):
    hist = array('i')
    try:
      f = open(name + '.txt', 'r')
    except: 
        print("file not found") 
        _hist = [0]
        return _hist
    for line in f:
        hist.append(int(line))
    f.close()
    return hist
    
#1st problem
draw_triangle(3)

#2nd problem
h1 = [1, 2, 3, 4 , 5]
h2 = [10, 11, 12, 13, 14]
print("расстояние = ", hist_distance(h1, h2)) 

#3rd problem
serialisaition(h1, "h1")
serialisaition(h2, "h2")

#4th problem
h3 = de_serialisaition("h1")
h4 = de_serialisaition("h2")
print("расстояние = ", hist_distance(h1, h2))
