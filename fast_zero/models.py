from datetime import datetime
from sqlalchemy.orm import (
    Mapped, mapped_as_dataclass, registry, mapped_column, relationship
)
from sqlalchemy import func, ForeignKey

table_registry = registry()


@mapped_as_dataclass(table_registry)
class User:
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    books: Mapped[list['Book']] = relationship(
        init=False,
        cascade='all, delete-orphan',
        lazy='selectin',
    )

    
@mapped_as_dataclass(table_registry)
class Book:
    __tablename__ = "books"

    book_id: Mapped[int] = mapped_column(init=False, primary_key=True)

    # Foreign key: cada Book pertence a UM User
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    book_name: Mapped[str]
    book_description: Mapped[str]

    



























