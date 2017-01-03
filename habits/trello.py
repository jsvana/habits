"""
Trello API wrapper because the official one isn't Python3-compatible :(
"""
from inflection import (
    camelize,
    pluralize,
    singularize,
    tableize,
)
import requests


from . import config


API_BASE = 'https://api.trello.com/1'


class Gettable(object):
    """
    Convenience around a Trello API object and does nasty magic
    """

    # Map of child object name -> child property list
    CHILDREN = {}

    # List of properties to get
    FIELDS = []

    def __init__(self, data):
        # TODO(jsvana): this is horribly inefficient as it fetches each child
        # object by ID in a separate API call. Should instead call the batch
        # endpoints.

        # Populate children
        for key in self.CHILDREN:
            if key not in data:
                continue

            values = {}
            child = data.pop(key)
            for item in child:
                klass = globals()[camelize(singularize(key))]
                values[item['name']] = klass.get(item['id'])

            # Add child names to class for convenience
            setattr(self, key, values)
            self.add_getter(key)

        for key, value in data.items():
            setattr(self, key, value)

    def add_getter(self, key):
        """
        Creates a getter for a child with a specific key
        """
        def get_item(name):
            values = getattr(self, key, {})
            if name not in values:
                raise ValueError(
                    'Unknown {} "{}"'.format(
                        singularize(key),
                        name,
                    ),
                )
            return values[name]

        setattr(self, singularize(key), get_item)

    @classmethod
    def base_url(cls, obj_id):
        return API_BASE + '/' + tableize(cls.__name__) + '/' + obj_id

    @classmethod
    def get(cls, obj_id):
        """
        Get the given object by ID from the API
        """
        url = cls.base_url(obj_id)
        params = {
            'fields': ','.join(cls.FIELDS),
            'key': config.trello['key'],
            'token': config.trello['token'],
        }
        for child_name, child_props in cls.CHILDREN.items():
            params[child_name] = 'open'
            params['{}_fields'.format(singularize(child_name))] = ','.join(
                child_props,
            )

        r = requests.get(url, params=params)
        return cls(r.json())


class Board(Gettable):
    """
    Trello Board wrapper
    """

    CHILDREN = {
        'lists': ['name'],
    }
    FIELDS = ['name', 'desc']


class List(Gettable):
    """
    Trello List wrapper
    """

    CHILDREN = {
        'cards': ['name'],
    }
    FIELDS = ['name']


class Card(Gettable):
    """
    Trello Card wrapper
    """

    CHILDREN = {}
    FIELDS = ['name']

    def comment(self, message):
        print(self.base_url(self.id) + '/actions/comments')
        r = requests.post(
            self.base_url(self.id) + '/actions/comments',
            data={
                'text': message,
                'key': config.trello['key'],
                'token': config.trello['token'],
            },
        )
        return r.json()
