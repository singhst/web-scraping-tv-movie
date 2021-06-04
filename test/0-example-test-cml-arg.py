#!/usr/bin/python
"""
https://www.tutorialspoint.com/python/python_command_line_arguments.htm
"""

import sys, getopt

def main(argv):
    print(argv)

    inputfile = ''
    outputfile = ''
    
    try:
        argumentList = argv

        # the colon `:` behind an arg (i.e. letter) = this arg has option
        # i.e.  if behind `-h` don't hv option         ==> `$ test.py -h` shows no errors
        #       if behind `-i or -o` don't hv option   ==> `$ test.py -i` shows errors  
        #                                              ==> `$ test.py -i XX` shows NO errors
        shortopts = "hi:o:"     
        long_options = ["ifile=", "ofile="]

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