import os

def folderExist(path: str) -> bool:
    """Check the folder exists or not
    """
    # print('os.path.exists(path)=',os.path.exists(path))
    return os.path.exists(path)


def folderCreate(path: str,
                 foldername: str = ''):
    """
    Return
    ------
    `str`, path of the folder.

    https://www.geeksforgeeks.org/create-a-directory-in-python/
    """
    path = os.path.join(path, foldername)

    if not folderExist(path):
        os.makedirs(path)
        print(f"> creates {path}")
    else:
        print(f"> folder existed, {path}")

    return path

