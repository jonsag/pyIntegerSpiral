#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import sys, getopt, os

import math

from modules import onError, usage

try:
    myopts, args = getopt.getopt(sys.argv[1:],
                                 's'
                                 'i'
                                 'r:'
                                 'p:'
                                 'm'
                                 'e:'
                                 'o:'
                                 'vh',
                                 ['screen', 'image', 'resolution=', 'points=', 'markstart', 
                                  'plotevery=', 'offset=', 
                                  'verbose', 'help'])

except getopt.GetoptError as e:
    onError(1, str(e))

if len(sys.argv) == 1:  # no options passed
    onError(2, 2)
    
plotToScreen = False
plotToImage = False
resolution = 10
numberOfPoints = 0
markStart = False
plotEvery = 0
plotEveryOffset = 0
verbose = False
    
for option, argument in myopts:
    if option in ('-s', '--screen'):
        plotToScreen = True
    elif option in ('-i', '--image'):
        plotToImage = True
    elif option in ('-r', '--resolution'):
        resolution = int(argument)
    elif option in ('-p', '--points'):
        numberOfPoints = int(argument)
    elif option in ('-m', '--markstart'):
        markStart = True
    elif option in ('-e', '--plotevery'):
        plotEvery = int(argument)
    elif option in ('-o', '--offset'):
        plotEveryOffset = int(argument)
    elif option in ('-v', '--verbose'):  # verbose output
        verbose = True
    elif option in ('-h', '--help'):  # display help text
        usage(0)
        
if not numberOfPoints:
    numberOfPoints = resolution * resolution * 4

if plotToScreen:
    import matplotlib.pyplot as plt
    plt.axis([-resolution, resolution, -resolution, resolution])

if plotToImage:
    from PIL import Image, ImageDraw
    import time
    
    img = Image.new('RGB', (resolution * 2, resolution * 2), color = 'white')
    draw = ImageDraw.Draw(img)
    
    timeStamp = time.strftime("%Y%m%d-%H:%M:%S")
    imageFormat = "bmp"
    imageName = "%s_%s.%s" % ("Filename", timeStamp, imageFormat)
    if verbose:
        print "Plotting to image file: %s\n" % imageName
        
if plotEvery:
    plotEveryCount = 1
    if plotEveryOffset:
        plotEveryCount = 11 - plotEveryOffset
    if verbose:
        print "\nWill plot every %s points\n" % plotEvery
        
oldCircle = -1
circle = 0

sideLength = 1

# circle        0    1    2    3    4    5
# sideLength    1    3    5    7    9
# points        1    8    16   24   32
#            a(n) = [x^(2*n)] ((1 + x)/(1 - x))^2

#    1    2    3    4    5    6    7    8    9    10    11    12    13    14    15    16    17    18    19
# x  0    1    1    0    -1   -1   -1   0    1    2     2     2     2     1     0     -1    -2    -2    -2
# https://oeis.org/A174344
# a(1) = 0, a(n) = a(n-1) + sin(mod(floor(sqrt(4*(n-2)+1)),4)*Pi/2)

# y  0    0    1    1    1    0    -1   -1   -1   -1    0     1     2     2     2     2     2     1     0
# https://oeis.org/A274923
# a(1) = 0, a(n) = a(n-1) + cos(mod(floor(sqrt(4*(n-2)+1)),4)*Pi/2)



for point in range(1, numberOfPoints):

    if oldCircle != circle:
        if verbose:
            print "Circle: %s" % circle
            print "Side length: %s" % (2 * circle + 1)
            
            if circle == 0:
                points = 1
            else:
                points = (8 + ( circle - 1 ) * 8)
            print "Points: %s" % points
            print "--------------------"
        
        oldCircle = circle
    
    pointFill = "black"
    
    if point == 1:
        x = 0
        y = 0
    else:
        x = x + int( math.sin( math.floor( math.sqrt( 4 * ( point - 2 ) + 1 ) % 4 ) * math.pi / 2 ))
        y = y + int( round(math.cos( math.floor( math.sqrt( 4 * ( point - 2 ) + 1 ) % 4 ) * math.pi / 2 )))
        
    if verbose:
        print "--- Point number: %s" % point
        print "    x: %s" % x
        print "    y: %s" % y
    
    plot = False
    
    if plotEvery != 0:
        if plotEveryCount == ( plotEvery ):
            plot = True
            plotEveryCount = 1
        else:
            plotEveryCount += 1
        if x == 0 and y == 0:
            pointFill = "green"
    elif markStart and x == 0 and y == 0:
        plot = True
        pointFill = "red"
            
    if plot:
        if verbose:
            print "+++ Will plot this point"
        if plotToScreen:
            plt.scatter(x, y, s = 1)
        if plotToImage:
            draw.point(( x + resolution, y + resolution ), fill = pointFill)

    sideLength += 2
    
    if plotToScreen:
        plt.pause(0.01)
    

    
if plotToScreen:
    plt.show()   
if plotToImage:
    img.save(imageName)
    
print "Parsed %s points" % point
    
    
    
    
    
