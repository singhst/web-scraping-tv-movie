"""
https://stackoverflow.com/questions/21564625/removing-everything-except-letters-and-spaces-from-string-in-python3-3
"""

import re


def translateToUrlPath(domain: str,
                       movie_or_show: str,
                       title: str,
                       year: str):
    """
    Translate a movie/TV show to Reelgood url path.

    Parameters
    ------
    `domain`: 
        `str`, e.g. https://reelgood.com/

    `movie_or_show`:
        `str`, `movie` or `show`, no 

    `title`:
        `str`, `Jim & Andy: The Great Beyond- Featuring a Very Special, Contractually Obligated Mention of Tony Clifton`

    `year`:
        `str`, `2017`
    """

    # print('in translateToUrlPath')

    # remove title's symbols ==> keep only letter, number and space char
    title = re.sub(r'[^a-zA-Z0-9 ]+', '', title)

    # remove double space chars, 
    # e.g.  "Jim & Andy: The" 
    #       ==> "Jim  Andy The",    have 2 space chars 
    #       ==> "Jim Andy The",     keep only 1 space 
    title = title.replace('  ', ' ')
    
    # replace space to hyphen
    title = title.lower().replace(' ', '-')

    return f"{domain}/{movie_or_show}/{title}-{year}"


if __name__ == "__main__":
    # https://reelgood.com/movie/the-intouchables-2011
    domain = "https://reelgood.com"
    movie_or_show = "movie"
    # title = "The Intouchables"
    # title = "Howl's Moving Castle"
    title = "Jim & Andy: The Great Beyond- Featuring a Very Special, Contractually Obligated Mention of Tony Clifton"
    year = "2011"
    url = translateToUrlPath(domain, movie_or_show, title, year)
    print(url)
