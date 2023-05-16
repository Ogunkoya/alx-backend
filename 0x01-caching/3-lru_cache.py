#!/usr/bin/python3
""" BaseCaching module
"""
from base_caching import BaseCaching

class LRUCache(BaseCaching):
    def __init__(self):
        super().__init__()
        self.usage_order = []

    def put(self, key, item):
        if key is None or item is None:
            return

        if len(self.cache_data) >= self.MAX_ITEMS:
            # Discard the least recently used item (LRU)
            discarded_key = self.usage_order[0]
            del self.cache_data[discarded_key]
            self.usage_order.pop(0)
            print(f"DISCARD: {discarded_key}")

        self.cache_data[key] = item
        self.usage_order.append(key)

    def get(self, key):
        if key is None or key not in self.cache_data:
            return None

        # Update usage order
        self.usage_order.remove(key)
        self.usage_order.append(key)

        return self.cache_data[key]
