#!/usr/bin/python3
""" BaseCaching module
"""
from base_caching import BaseCaching
class BasicCache(BaseCaching):
    """ BaseCaching defines:
      - constants of your caching system
      - where your data are stored (in a dictionary)
    """
    def put(self, key, item):
        if key is None or item is None:
            return
        self.cache_data[key] = item

    def get(self, key):
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]