from dataclasses import dataclass
from typing import Callable, Generator, Generic, List, TypeVar, Union

Result = TypeVar("Result")


@dataclass
class PaginatedResults(Generic[Result]):
    count: int
    results: List[Result]


def get_all_results(
    paginated_api: Callable[[int, Union[int, None]], PaginatedResults[Result]],
    page_size: Union[int, None] = None,
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

        offset = count
