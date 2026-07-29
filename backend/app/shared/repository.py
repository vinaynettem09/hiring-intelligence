"""Tiny repository bases.

Deliberately NOT a generic CRUD repository. `Repository` only holds the
request-scoped session; concrete repositories (e.g. OrganizationRepository) add
domain-language methods. `TenantScopedRepository` adds a small tenant filter
helper for tenant-owned entities (used from Story 1.1 onward — organizations are
the tenant root and do not use it).
"""

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession


class Repository:
    """Base: carries the request-scoped session. Never opens or commits it."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session


class TenantScopedRepository(Repository):
    """Base for tenant-owned entities: carries the tenant and a filter helper."""

    def __init__(self, session: AsyncSession, tenant_id: str) -> None:
        super().__init__(session)
        self.tenant_id = tenant_id

    def _scoped(self, stmt: Any, tenant_column: Any) -> Any:
        """Apply the tenant filter to a SELECT so callers cannot forget it.

        (Typed loosely on purpose — SQLAlchemy's Select generics add friction for
        no safety here.)
        """
        return stmt.where(tenant_column == self.tenant_id)
