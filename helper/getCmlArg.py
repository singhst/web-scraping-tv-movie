import sys
import getopt

def getCmlArg() -> str:
    """Get the arguments from command line. Return `str` 'tv' / 'curated/trending-picks' or 'movies' . 'curated/trending-movies'
    """
    argv = sys.argv[1:]
    # print("argv =", argv)

    if not argv:
        print('> Please enter arg, `test.py -t OR -m <trend (optional)>`')
        sys.exit(2)

    try:
        argumentList = argv
        shortopts = "htm"
        long_options = ["tv", "movie"]
        opts, args = getopt.getopt(argumentList, shortopts, long_options)

    except getopt.GetoptError:
        print('> Wrong arg, `test.py -t OR -m <trend (optional)>`')
        sys.exit(2)

    # print("opts =", opts)
    # print("args =", args)

    # for opt, arg in opts:
    opt = opts[0][0]
    if opt == '-h':
        print('> in `-h`, `test.py -t OR -m <trend (optional)>`')
        sys.exit()
    elif opt in ("-t", "-tv", "-tvshow", "-tvshows"):
        try:
            if args[0] in ["trend", "trending"]:
                return 'curated/trending-picks', 'trending-tv'
        except:
            return 'tv', 'tv'
    elif opt in ("-m", "-movie", "-movies"):
        try:
            if args[0] in ["trend", "trending"]:
                return 'curated/trending-movies', 'trending-movies'
        except:
            return 'movies', 'movies'
    # print('url path is "', url_path)

    print('> wrong argument, `test.py -t OR -m <trend (optional)>`')
    sys.exit()


if __name__ == "__main__":
    getCmlArg()