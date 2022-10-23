from distutils.sysconfig import EXEC_PREFIX
from collections import Counter
from PIL import Image #image prossesing API
from numpy import asarray #deafault numpy library
import math #deafault math library
import os

size = 100, 100


#this function calculates distance between 2 vectors 
def hist_distance(hist1, hist2):
    if len(hist1) - len(hist2) != 0:
        print("vectors length doesent match")
        return
    squared_sum = 0.0
    for i in range(1, len(hist1)): squared_sum += (int(hist1[i]) - int(hist2[i])) * int((hist1[i]) - int(hist2[i])) #range changed from 0 to 1 because of new hist file system, where hist[0] = type
    return math.sqrt(squared_sum)

#this function creates a file of hist with defined name
def serialisaition(_type, hist1, name):
      f = open('histograms/' + name + '.txt', 'w')
      f.write(str(_type) + '\n')
      for i in range(0, len(hist1)):
          f.write(str(hist1[i]) + '\n')
      f.close()
      print('file created with name = ',name,'.txt')

#this function reads a file of hist with defined name
def de_serialisaition(name):
    hist = []
    try:
      f = open('histograms/' + name, 'r')
    except: 
        print("file not found") 
        _hist = [0]
        return _hist
    for line in f:
        hist.append(line)
    f.close()
    return hist

#this function creates a file of image histogramm red chanel
def parsing_data(ndata, _type, name):
    h1 = []
    for item in ndata:
        for data in item:
            try: h1.append(data[0]) 
            except: data[0, 0] #adding only red channel to lower space usage
    serialisaition(_type, h1, name)
    return h1

#this function creates a multiple files from test data (learning)
def setting_up():
    #deleting previous histograms
    h_files = os.listdir('histograms')
    for it in range(0, len(h_files)):
        os.remove('histograms/' + h_files[it])
        print('file ' + h_files[it] + ' has been deleted')
    
    headers = os.listdir('TestData') #creating headers from folders names
    file_numbering = 0
    for i in range(0, len(headers)):
        dir_list = os.listdir('TestData/' + headers[i])

        #going through directory
        for j in range(0, len(dir_list)):
            _img = Image.open('TestData/' + headers[i] + '/' + dir_list[j]) #opening image in derictory
            img = _img.resize(size) #resizing image
            img = img.convert('RGB') #converting to RGB file format

            numpydata = asarray(img) #parsing image into array of pixels with r g b channels
            parsing_data(numpydata, headers[i], 'h' + str(file_numbering))
            file_numbering += 1
    print('\n learning done!')

#logic for finding out what type is it
def type_finding_out(path):
        

    try:
        #prosessing user image
        _img = Image.open(path) 
        img = _img.resize(size)
        img = img.convert('RGB')
        numpydata = asarray(img)
        hu = parsing_data(numpydata, 'user', 'user')

        _files = os.listdir('histograms')

        result_min = [999999999, 999999999, 999999999]
        result_types = ["type", "type", "type"]
        for i in range(0, len(_files)):
            if _files[i] != 'user.txt':
                hpr = de_serialisaition(_files[i])#reading file
                _type = hpr[0]
                hpr.remove(hpr[0]) #removing type from list
                distance = hist_distance(hu, hpr)

                #3 min distances + types
                if distance < result_min[2] and distance > result_min[1] and distance > result_min[0]:
                    result_min[2] = distance
                    result_types[2] = _type
                elif distance < result_min[1] and distance > result_min[0] and distance < result_min[1]:
                    result_min[1] = distance
                    result_types[1] = _type
                elif distance < result_min[0]: 
                    result_min[0] = distance
                    result_types[0] = _type
                        
        counter = Counter(result_types) #creating dictionary for most repeated types
                    
        print('\n')
        print(result_min)
        print('\n')
        print(result_types)
        print('\n this is a ' + max(counter, key=counter.get)) #printing max value in dctionary

           
    except: print('SMH((( FNF FR') 



paths = ['learn', 'user.png', 'user1.png', 'user2.png'] #path used for demo
j = 0
while j < 4:
    print('\ntype desired file path \nor type ''learn'' to learn new images \n')
    #path = input() #user-defined path

    path = paths[j] #demo-defined path
    print(path + '\n')

    #program controls, we don't need it for demo
    if path == 'learn': setting_up()
    elif path == 'stop': break
    else:
        type_finding_out(path)
    j += 1

        