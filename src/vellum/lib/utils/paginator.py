from dataclasses import dataclass
from typing import Callable, Generic, TypeVar


Result = TypeVar("Result")


@dataclass
class PaginatedResults(Generic[Result]):
    count: int
    results: list[Result]


def get_all_results(
    paginated_api: Callable[[int, int | None], PaginatedResults[Result]], page_size: int | None = None
) -> list[Result]:
    offset = 0
    results = []
    while True:
        paginated_results = paginated_api(offset, page_size)
        results.extend(paginated_results.results)
        if paginated_results.count <= len(results):
            break
        offset += page_size
    return results
