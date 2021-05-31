def translateToUrlPath(domain: str,
                        movie_or_show: str,
                        title: str,
                        year: str):
    """
    Translate a movie/TV show to Reelgood url path
    """

    # print('in translateToUrlPath')
    
    title = title.lower().replace(' ', '-')

    return f"{domain}/{movie_or_show}/{title}-{year}"


if __name__ == "__main__":
    # https://reelgood.com/movie/the-intouchables-2011
    domain = "https://reelgood.com"
    movie_or_show = "movie"
    title = "The Intouchables"
    year = "2011"
    url = translateToUrlPath(domain,movie_or_show,title,year)
    print(url)