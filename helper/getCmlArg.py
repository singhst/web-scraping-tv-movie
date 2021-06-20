"""
https://www.tutorialspoint.com/python/python_command_line_arguments.htm
"""

from typing import Iterable
import sys
import getopt

def getCmlArg() -> Iterable[str]:
    """Get the arguments from command line. 
    
    Return 
    ---
    `list(str)`

    format: `[<url_path>, <folder_name>]

    Example
    ---
    return 
        `['curated/trending-picks', 'trending-tv']`

        OR `['tv', 'tv']` 

        OR `['curated/trending-movies', 'trending-movies']`
        
        OR `['movies', 'movies']`
    """
    argv = sys.argv[1:]
    # print("argv =", argv)

    if not argv:
        print('> Please enter arg, `test.py -h OR -t OR -m <trend (optional)>`')
        sys.exit(2)

    try:
        argumentList = argv
        shortopts = "htm"
        long_options = ["tv=", "movie="]
        opts, args = getopt.getopt(argumentList, shortopts, long_options)

    except getopt.GetoptError:
        print('> Wrong arg, `test.py -h OR -t OR -m <trend (optional)>`')
        sys.exit(2)

    # print("opts =", opts)
    # print("args =", args)

    # for opt, arg in opts:
    opt = opts[0][0]
    if opt == '-h':
        print('> in `-h`, `test.py -t OR -m <trend (optional)>`')
        print()
        print('\t`-h`: Help\n')
        print('\t`-t`: Scrape TV shows\n')
        print('\t`-m`: Scrape movies\n') 
        print('\t`-t` OR `-m` trend (optional)\n')
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

    print('> wrong argument, `test.py -h OR -t OR -m <trend (optional)>`')
    sys.exit()



if __name__ == "__main__":

    url_path, folder_name = getCmlArg()

    print(f"url_path={url_path}, folder_name={folder_name}")