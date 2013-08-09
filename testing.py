#!/usr/bin/python

## copyright: Christian Berendt <berendt@b1-systems.de>, 2013.
##    author: Christian Berendt <berendt@b1-systems.de>, 2013.
##   license: Apache License, Version 2.0

import csv

BLACK = 0
WHITE = 1
GREEN = 2
RED = 3

color = [
"0 0 0",
"255 255 255",
"0 255 0",
"255 0 0"
]

def outputImage(data, height, width):

    result = ""
    result += "P3\n"
    result += "%d %d\n" % (width, height)
    result += "255\n"

    h = 0
    while h < height:
        w = 0
        rline = []
        while w < width:
            line = data[w]
            rline.append(color[line[h]])
            w += 1

        result += " ".join(rline) + "\n"
        h += 1

    return result

def loadData():

    incoming = open('EURUSD.txt', 'rb')
    reader = csv.reader(incoming)
    data = list()

    for row in reader:
        o = int(float(row[3]) * 10000)
        h = int(float(row[4]) * 10000)
        l = int(float(row[5]) * 10000)
        c = int(float(row[6]) * 10000)
        data.append([o, h, l, c])

    return data

def convert(data):

    x = 0
    result = list()

    width = len(data)
    maximum = max(map(lambda x: x[1], data))
    minimum = min(map(lambda x: x[2], data))
    height  = maximum - minimum

    for entry in data:
        o = entry[0]
        h = entry[1]
        l = entry[2]
        c = entry[3]

        start_1 = maximum - h
        stop_1 = start_1 + (h - l) - 1

        if o > c:
            start_2 = maximum - o
            stop_2 = start_2 + (o - c)

        if o < c:
            start_2 = maximum - c
            stop_2 = start_2 + (c - o)

        row = []
        for y in xrange(0, height):
            value = WHITE
            if y >= start_1 and y <= stop_1:
                value = BLACK

                if o > c and y >= start_2 and y <= stop_2:
                    value = GREEN

                if o < c and y >= start_2 and y <= stop_2:
                    value = RED

            row.append(value)
        result.append(row)
        x += 1
    return(result, height, width)

data = loadData()
for x in xrange(0, 25000):
    result, height, width = convert(data[x:x+20])
    f = open("%s.ppm" % x, 'w+')
    f.write(outputImage(result, height, width))
    f.close()
