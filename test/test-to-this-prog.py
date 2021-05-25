#!/usr/bin/python

import sys, getopt

def getCmlArg(argv):
    # print("argv =", argv)

    url_path = ''
    
    if not argv:
        print('> Please enter arg, `main.py -h OR -t OR -m`')
        sys.exit(2)

    try:
        argumentList = argv
        shortopts = "htm"     
        long_options = ["tv", "movie"]
        opts, args = getopt.getopt(argumentList, shortopts, long_options)

    except getopt.GetoptError:
        print('> Wrong arg, `test.py -h OR -t OR -m`')
        sys.exit(2)

    # print("opts =", opts)

    for opt, arg in opts:
        if opt == '-h':
            print('> in `-h`, `test.py -t OR -m`')
            sys.exit()
        elif opt in ("-t", "-tv", "-tvshow", "-tvshows"):
            url_path = 'tv'
        elif opt in ("-m", "-movie", "-movies"):
            url_path = 'movies'
    # print('url path is "', url_path)

    return url_path


def main():
    url_path = getCmlArg(sys.argv[1:])
    print("url_path =", url_path)

if __name__ == "__main__":
    main()