#!/usr/bin/env python3
import csv
import math
from typing import List


def index_range(page: int, page_size: int) -> tuple[int, int]:
    start_index = (page - 1) * page_size
    end_index = start_index + page_size - 1
    return start_index, end_index


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        assert isinstance(page, int) and page > 0, "Page argument must be a positive integer"
        assert isinstance(page_size, int) and page_size > 0, "Page size argument must be a positive integer"

        dataset = self.dataset()
        num_pages = math.ceil(len(dataset) / page_size)

        if page > num_pages:
            return []

        start_index, end_index = index_range(page, page_size)
        return dataset[start_index:end_index+1]
