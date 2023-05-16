#!/usr/bin/python3
""" BaseCaching module
"""
from base_caching import BaseCaching
from collections import defaultdict

class LFUCache(BaseCaching):
    def __init__(self):
        super().__init__()
        self.frequency = defaultdict(int)
        self.usage_order = []

    def put(self, key, item):
        if key is None or item is None:
            return

        if len(self.cache_data) >= self.MAX_ITEMS:
            min_frequency = min(self.frequency.values())
            least_frequent_keys = [
                key for key in self.frequency if self.frequency[key] == min_frequency
            ]

            if len(least_frequent_keys) > 1:
                # Discard the least recently used among the least frequent items (LRU)
                discarded_key = self.usage_order[0]
                least_frequent_keys.remove(discarded_key)

            discarded_key = least_frequent_keys[0]
            del self.cache_data[discarded_key]
            del self.frequency[discarded_key]
            self.usage_order.remove(discarded_key)
            print(f"DISCARD: {discarded_key}")

        self.cache_data[key] = item
        self.frequency[key] += 1
        self.usage_order.append(key)

    def get(self, key):
        if key is None or key not in self.cache_data:
            return None

        # Update frequency and usage order
        self.frequency[key] += 1
        self.usage_order.remove(key)
        self.usage_order.append(key)

        return self.cache_data[key]
