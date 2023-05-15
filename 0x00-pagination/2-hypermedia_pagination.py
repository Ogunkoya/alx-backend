#!/usr/bin/env python3
import csv
import math
from typing import List


def index_range(page: int, page_size: int) -> tuple[int, int]:
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
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

    def get_hyper(self, page: int = 1, page_size: int = 10) -> dict:
        assert isinstance(page, int) and page > 0, "Page argument must be a positive integer"
        assert isinstance(page_size, int) and page_size > 0, "Page size argument must be a positive integer"

        dataset = self.get_page(page, page_size)
        num_pages = math.ceil(len(self.dataset()) / page_size)

        next_page = page + 1 if page < num_pages else None
        prev_page = page - 1 if page > 1 else None

        return {
            "page_size": len(dataset),
            "page": page,
            "data": dataset,
            "next_page": next_page,
            "prev_page": prev_page,
            "total_pages": num_pages
        }