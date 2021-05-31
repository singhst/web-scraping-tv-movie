"""
[
    {
        'id': 1,
        'type': 'movie' or 'show',
        'title': 'xxx',
        'year': 'nnnn',
        'description': 'xxx yyyyyy zzzz',
        'links': [
            'url1',
            'url2',
            ...
        ]
    },
    {
        xxx
    },
    ...
]
"""

from typing import Iterable

# define a class to standardize the data structure
class item():
    def __init__(self,
                 id: str,
                 type: str = '',
                 title: str = '',
                 year: str = '',
                 description: str = '',
                 links: Iterable[str] = ['']
                 ):

        self._item = {
            'id': id,
            'type': type,
            'title': title,
            'year': year,
            'description': description,
            'links': links
        }

    def getItem(self) -> dict:
        return self._item


# class for importing by others
class tempStorage(item):

    def __init__(self):
        self.item = []

    def addItem(self,
            type: str,
            title: str,
            year: str,
            description: str,
            links: Iterable[str] = ['']
            ):

        # if empty, i.e. len(self.description) = 0
        #   ==> id for new item = 0
        id = int(len(self.item))

        super().__init__(id, type, title, year, description, links)
        _ = super().getItem()
        # print(_)
        # print(self.item)
        self.item.append(_)

    def getStoredItems(self) -> list:
        return self.item


if __name__ == "__main__":
    storage = tempStorage()

    storage.addItem('type', 'title', 'year', 'des', ['url'])
    storage.addItem('type', 'title', 'year', 'des')

    print(storage.getStoredItems())

