#!/usr/bin/python3
""" BaseCaching module
"""
from base_caching import BaseCaching

class MRUCache(BaseCaching):
    def __init__(self):
        super().__init__()
        self.usage_order = []

    def put(self, key, item):
        if key is None or item is None:
            return

        if len(self.cache_data) >= self.MAX_ITEMS:
            # Discard the most recently used item (MRU)
            discarded_key = self.usage_order[-1]
            del self.cache_data[discarded_key]
            self.usage_order.pop()
            print(f"DISCARD: {discarded_key}")

        self.cache_data[key] = item
        self.usage_order.insert(0, key)

    def get(self, key):
        if key is None or key not in self.cache_data:
            return None

        # Update usage order
        self.usage_order.remove(key)
        self.usage_order.insert(0, key)

        return self.cache_data[key]
