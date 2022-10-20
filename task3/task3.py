#from unittest import result 
from PIL import Image
from numpy import asarray
import math
number_of_items = 7 #number of items

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
    hist = []
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

#this function creates a file of image histogramm 
def parsing_data(ndata, name):
    h1 = []
    for item in ndata:
        for data in item:
            h1.append(data[0])
    serialisaition(h1, name)
    return h1

#this function creates a multiple files from test data (learning)
def setting_up():
    for i in range(1, number_of_items + 1):
        img = Image.open('TestData/triang/tr' + str(i) + '.png')
        numpydata = asarray(img)
        parsing_data(numpydata, 'tr' + str(i))

    for i in range(1, number_of_items + 1):
        img = Image.open('TestData/circles/s' + str(i) + '.png')
        numpydata = asarray(img)
        parsing_data(numpydata, 's' + str(i))

    for i in range(1, number_of_items + 1):
        img = Image.open('TestData/squares/sq' + str(i) + '.png')
        numpydata = asarray(img)
        parsing_data(numpydata, 'sq' + str(i))

#logick for finding out what type is it
def type_finding_out():
    while 1 == 1:
        path = input()
        result_min = 999999999
        result_type = 'none'
        try:
            img = Image.open(path)
            numpydata = asarray(img)
            hu = parsing_data(numpydata, 'user')
            for i in range(1, number_of_items + 1):
                hsq = de_serialisaition('sq' + str(i))

                var_sq = hist_distance(hu, hsq)
                if var_sq < result_min:
                    result_min = var_sq
                    result_type = 'this is a square'

                hs = de_serialisaition('s' + str(i))
                var_s = hist_distance(hu, hs)
                if var_s < result_min:
                    result_min = var_s
                    result_type = 'this is a circle'

                htr = de_serialisaition('tr' + str(i))
                var_tr = hist_distance(hu, htr)
                if var_tr < result_min:
                    result_min = var_tr
                    result_type = 'this is a triangle'

            print(result_type)

        except: print('file not found')

type_finding_out()