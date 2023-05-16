#!/usr/bin/python3
""" BaseCaching module
"""
from base_caching import BaseCaching
class LIFOCache(BaseCaching):
    def __init__(self):
        super().__init__()

    def put(self, key, item):
        if key is None or item is None:
            return
        
        if len(self.cache_data) >= self.MAX_ITEMS:
            # Get the last item inserted into the cache (LIFO)
            discarded_key = list(self.cache_data.keys())[-1]
            del self.cache_data[discarded_key]
            print(f"DISCARD: {discarded_key}")
        
        self.cache_data[key] = item

    def get(self, key):
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]