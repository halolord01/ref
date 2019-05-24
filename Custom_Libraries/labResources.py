import numpy as np
import matplotlib.pylab as plt
import os
import csv

def average(l):
    return sum(l)/len(l)

def derive(alpha, ts):
    firstIter = True
    w = []
    for index,valY in enumerate(alpha):
        if firstIter:
            da = valY
            firstIter = False
        else:
            da = valY - alpha[index-1]
        
        w.append(da/ts)
        # w.append(da/(1/ts))
    return w



def fGather(fName, delim = '\t', tl = False):
    fLine = 0
    tCSV,eCSV,lCSV = [],[],[]
    with open (fName, 'r') as f:
        result = [[] for o in range(len(f.readline().split(delim)))]
        f.seek(0)
        for index, ins in enumerate(f):
            try:

                float(ins.split(delim)[0])
                # unpack the line into temp variables, then add onto the list
                dataLine = ins.split(delim)
                for i in range(len(result)):
                    result[i].append(float(dataLine[i]))

            except:
                titleLine = ins.split(delim)




            # try:
            #     pass
            # except Exception, e:
            #     raise
            # else:
            #     pass
            # finally:
            #     pass
    if tl:
        return result, titleLine
    else:
        return result

def plotter(*args, **kwargs):
    plotnums = kwargs["plots"]
    plt.figure(kwargs["title"], tight_layout = True)
    if ("xlab" or "ylab") in kwargs:
        plt.xlabel(kwargs["xlab"])
        plt.ylabel(kwargs["ylab"])
    
    plt.title(kwargs["title"])
    for i in range(plotnums):
        
        xName = "x" + str(i + 1)
        yName = "y" + str(i + 1)
        LABEL = "label" + str(i + 1)

        x = kwargs[xName]
        y = kwargs[yName]
        # plt.subplot()
        plt.plot(x,y,label=kwargs[LABEL])
        plt.grid(True)
        # plt.xlabel
        # plt.ylabel
    # plt.legend(loc = 4)
    plt.legend()
    plt.show()
    pass


# This function gets data from the csv file, and returns a data structure

def read_csv(file_, header = True, delimiter = None):
    head_line = ''
    data = []
    with open(file_, 'r') as f:
        for i, line in enumerate(f):
            if i == 1:
                if header:
                    head_line = line.split(delimiter)
                data_ = [[] for x in range(len(line.split(delimiter)))]
            else:
                parsed_line = line.split(delimiter)
                for group, dat in zip(data_, parsed_line):
                    # high change to not work
                    group.append(dat)

            # if i ==1 and header:
            #     head_line = line.split(delimiter)
            # else:
            #     data.append(line.split(delimiter))

    if header:
        return data_, header
    else:
        return data_


# need one that takes in radiuses and everyhting
# otherwise the ares and lenghts wont be okay
def shearStress(moment, diam):
    j = (3.13159 / 2) * (diam ** 4 )
    torque = moment * (diam / 2) / j
    return torque

def shearStrain(phi, diam, length):
    return ((diam / 2) * phi) / length

def trimmer(*args, **kwargs):
    n = []
    for ins in args:
        n.append(ins[kwargs["start"]:kwargs["end"]])
    return n

