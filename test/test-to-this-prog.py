#!/usr/bin/python

import sys, getopt

def getCmlArg(argv) -> str:
    """Get the arguments from command line. Return `str` 'tv' / 'curated/trending-picks' or 'movies' . 'curated/trending-movies'
    """
    # print("argv =", argv)
    
    if not argv:
        print('> Please enter arg, `test.py -h OR -t OR -m <trend> (optional)`')
        sys.exit(2)

    try:
        argumentList = argv
        shortopts = "htm"
        long_options = ["tv", "movie"]
        opts, args = getopt.getopt(argumentList, shortopts, long_options)

    except getopt.GetoptError:
        print('> Wrong arg, `test.py -h OR -t OR -m <trend> (optional)`')
        sys.exit(2)

    # print("opts =", opts)
    # print("args =", args)

    # for opt, arg in opts:
    opt = opts[0][0]
    if opt == '-h':
        print('> in `-h`, `test.py -h OR -t OR -m <trend> (optional)`')
        sys.exit()
    elif opt in ("-t", "-tv", "-tvshow", "-tvshows"):
        try:
            if args[0] in ["trend", "trending"]:
                return 'curated/trending-picks', 'tv trending'
        except:
            return 'tv', 'tv'
    elif opt in ("-m", "-movie", "-movies"):
        try:
            if args[0] in ["trend", "trending"]:
                return 'curated/trending-movies', 'movies trending'
        except:
            return 'movies', 'movies'
    # print('url path is "', url_path)

    print('> wrong argument, `test.py -h OR -t OR -m <trend> (optional)`')
    sys.exit()


def main():
    url_path, folder_name = getCmlArg(sys.argv[1:])
    print("url_path =", url_path)
    print("folder_name =", folder_name)


if __name__ == "__main__":
    main()