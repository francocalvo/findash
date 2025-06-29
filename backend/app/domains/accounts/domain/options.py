"""Search options for accounts domain."""

import uuid
from enum import Enum

from app.constants import DEFAULT_PAGINATION_LIMIT


class SortOrder(Enum):
    """Enumeration for sorting order."""

    ASC = "asc"
    DESC = "desc"


class SearchFilters:
    """Options for searching accounts."""

    name: str | None = None
    type: str | None = None
    currency: str | None = None
    is_active: bool | None = None
    parent_id: uuid.UUID | None = None

    def __init__(
        self,
        name: str | None = None,
        type: str | None = None,
        currency: str | None = None,
        is_active: bool | None = None,
        parent_id: uuid.UUID | None = None,
    ):
        self.name = name if name else None
        self.type = type if type else None
        self.currency = currency if currency else None
        self.is_active = is_active
        self.parent_id = parent_id


class SearchPagination:
    """Options for paginating search results."""

    skip: int = 0
    limit: int = 50

    def __init__(self, skip: int = 0, limit: int = DEFAULT_PAGINATION_LIMIT):
        self.skip = skip
        self.limit = limit if limit > 0 else DEFAULT_PAGINATION_LIMIT


class SearchSorting:
    """Options for sorting search results."""

    field: str = "name"
    order: SortOrder = SortOrder.ASC

    def __init__(self, field: str = "name", order: SortOrder = SortOrder.ASC):
        self.field = field
        self.order = order


class SearchOptions:
    """Options for searching accounts."""

    filters: SearchFilters
    pagination: SearchPagination
    sorting: SearchSorting

    def __init__(self):
        self.filters = SearchFilters()
        self.pagination = SearchPagination(skip=0, limit=DEFAULT_PAGINATION_LIMIT)
        self.sorting = SearchSorting()

    def with_filters(self, filters: SearchFilters) -> "SearchOptions":
        """Create a new search with specified filters."""
        new_search = SearchOptions()
        new_search.filters = filters
        new_search.pagination = self.pagination
        new_search.sorting = self.sorting
        return new_search

    def with_pagination(self, pagination: SearchPagination) -> "SearchOptions":
        """Create a new search with specified pagination."""
        new_search = SearchOptions()
        new_search.filters = self.filters
        new_search.pagination = pagination
        new_search.sorting = self.sorting
        return new_search

    def with_sorting(self, sorting: SearchSorting) -> "SearchOptions":
        """Create a new search with specified sorting options."""
        new_search = SearchOptions()
        new_search.filters = self.filters
        new_search.pagination = self.pagination
        new_search.sorting = sorting
        return new_search
