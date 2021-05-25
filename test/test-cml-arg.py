#!/usr/bin/python

import sys, getopt

def main(argv):
    print(argv)

    inputfile = ''
    outputfile = ''
    
    try:
        argumentList = argv
        shortopts = "ahi:o:"     # the colon `:` behind an arg (i.e. letter) = this arg has option
        long_options = ["ifile=","ofile="]

        opts, args = getopt.getopt(argumentList, shortopts, long_options)

    except getopt.GetoptError:
        print('GetoptError> test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)

    print(opts)

    for opt, arg in opts:
        if opt == '-h':
            print('-h> test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    print('Input file is "', inputfile)
    print('Output file is "', outputfile)

if __name__ == "__main__":
    main(sys.argv[1:])