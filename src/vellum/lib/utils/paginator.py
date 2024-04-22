from dataclasses import dataclass
from typing import Callable, Generator, Generic, TypeVar


Result = TypeVar("Result")


@dataclass
class PaginatedResults(Generic[Result]):
    count: int
    results: list[Result]


def get_all_results(
    paginated_api: Callable[[int, int | None], PaginatedResults[Result]], page_size: int | None = None
) -> Generator[Result, None, None]:
    offset = 0
    count = 0
    while True:
        paginated_results = paginated_api(offset, page_size)
        for result in paginated_results.results:
            yield result
            count += 1

        if paginated_results.count <= count:
            break

        offset += page_size
