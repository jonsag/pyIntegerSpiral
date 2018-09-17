#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import ConfigParser, os, sys

config = ConfigParser.ConfigParser()  # define config file
config.read("%s/config.ini" % os.path.dirname(os.path.realpath(__file__)))  # read config file

def onError(errorCode, extra):
    print "\nError:"
    if errorCode == 1:
        print extra
        usage(errorCode)
    elif errorCode == 2:
        print "No options given"
        usage(errorCode)
        
def usage(exitCode):
    print "\nUsage:"
    print "----------------------------------------"
    print "%s -s (--screen)" % sys.argv[0]
    print "    Show output on screen via mathlibplot"
    print "%s -i (--image)" % sys.argv[0]
    print "    Plot output to image\n"
    
    print "%s -s (--screen) | -i (--image) -r (--resolution) z" % sys.argv[0]
    print "    Create grid with size -z:z X -z:z\n"
    
    print "%s -s (--screen) | -i (--image) -p (--points) z" % sys.argv[0]
    print "    Plot z points\n"
    
    print "%s -e (--plotevery) <x> [-o (--offset) <y>]" % sys.argv[0]
    print "    Plot every x point [ with y offset ]\n"
    
    print "%s -s (--screen) | -i (--image) -m (--markstart)" % sys.argv[0]
    print "    Mark zero point with color\n"
    
    print "%s -v (--verbose)" % sys.argv[0]
    print "    Verbose output"
    print "%s -h (--help)" % sys.argv[0]
    print "    Prints this"

    sys.exit(exitCode)