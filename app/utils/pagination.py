# ============================================================
# CyberShield — Pagination Utility
# ============================================================

from dataclasses import dataclass
from typing import Generic, TypeVar, Optional
from fastapi import Query

T = TypeVar("T")


@dataclass
class PageParams:
    page: int
    size: int

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.size

    @property
    def limit(self) -> int:
        return self.size


@dataclass
class PageResult(Generic[T]):
    items: list[T]
    total: int
    page: int
    size: int
    pages: int
    has_next: bool
    has_prev: bool

    @classmethod
    def create(
        cls,
        items: list[T],
        total: int,
        params: PageParams,
    ) -> "PageResult[T]":
        pages = max(1, -(-total // params.size))
        return cls(
            items=items,
            total=total,
            page=params.page,
            size=params.size,
            pages=pages,
            has_next=params.page < pages,
            has_prev=params.page > 1,
        )

    def to_dict(self) -> dict:
        return {
            "items": self.items,
            "pagination": {
                "total":    self.total,
                "page":     self.page,
                "size":     self.size,
                "pages":    self.pages,
                "has_next": self.has_next,
                "has_prev": self.has_prev,
            },
        }


def get_page_params(
    page: int = Query(default=1, ge=1, description="Page number"),
    size: int = Query(default=20, ge=1, le=100, description="Items per page"),
) -> PageParams:
    """FastAPI dependency for pagination parameters."""
    return PageParams(page=page, size=size)
