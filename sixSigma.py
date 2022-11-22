# Cp = USL-LSL/6sigma
import numpy as np
import math as mt
import matplotlib.pyplot as plt
import csv

huml = []
with open('bird.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    count = 0
    for row in csv_reader:
        if count == 0:
            pass
        elif row[1] == '':
            pass
        else:
            huml.append(float(row[1]))
        count = count+1

# Graphing function


def graph(array):
    mean = calcMean(array)
    std = calcSD(array)
    y_out = 1/(std * np.sqrt(2 * np.pi)) * \
        np.exp(- (array - mean)**2 / (2 * std**2))
    return y_out

# Normal.S.Distribution


def phi(x):
    return (1.0 + mt.erf(x / mt.sqrt(2.0))) / 2.0

# Mean


def calcMean(array):
    return np.mean(array)

# Standard Deviation


def calcSD(array):
    mean = calcMean(array)
    accumulator = 0
    for i in array:
        accumulator = accumulator + pow((mean - i), 2)
    sub = accumulator/(len(array)-1)

    return mt.sqrt(sub)

# Process capability


def calcSixSigma_cp(array, usl, lsl):
    range = usl-lsl
    sd = calcSD(array)
    return range/(6*sd)

# Zupper value


def calcZUpper(usl, array):
    sd = calcSD(array)
    mean = calcMean(array)

    return (usl-mean)/sd

# Zlower value


def calcZLower(lsl, array):
    sd = calcSD(array)
    mean = calcMean(array)

    return (mean - lsl)/sd

# Failure rate outside bounds from upper standard limit & lower standard limit


def ppm(array, lsl, usl):
    zl = calcZLower(lsl, array)
    zu = calcZUpper(usl, array)
    range = (1-phi(zl)) + (1-phi(zu))*1000000
    return range


newArray = huml
newArray.sort()

print("Failure rate is", ppm(huml, 0, 200), "per million")
y = graph(newArray)
plt.figure(figsize=(6, 6))
plt.plot(newArray, y, color='black', linestyle='solid')
plt.scatter(newArray, y, marker='o', s=25, color='red')
plt.show()
