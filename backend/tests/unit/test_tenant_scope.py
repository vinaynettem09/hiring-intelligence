"""Tenant-scope helper test.

Proves the shared tenant filter adds the correct WHERE clause, so tenant-owned
repositories (from Story 1.1) cannot forget it.
"""

from sqlalchemy import String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.shared.repository import TenantScopedRepository


class _Base(DeclarativeBase):  # test-only, isolated from the app's Base
    pass


class _Thing(_Base):
    __tablename__ = "_things"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(36))


async def test_scoped_adds_tenant_filter(session: AsyncSession) -> None:
    repo = TenantScopedRepository(session=session, tenant_id="tenant-abc")
    stmt = repo._scoped(select(_Thing), _Thing.tenant_id)
    sql = str(stmt.compile(compile_kwargs={"literal_binds": True}))
    assert "tenant_id" in sql
    assert "tenant-abc" in sql
