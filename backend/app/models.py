import uuid

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Shared properties
class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Properties to receive on item creation
class ItemCreate(ItemBase):
    pass


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="items")


# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int


# Base Transaction model
class TransactionBase(SQLModel):
    """Base model for all financial transactions."""
    date: str = Field(index=True)
    account: str = Field(index=True)
    payee: str | None = None
    narration: str
    amount_ars: float
    amount_usd: float

    class Config:
        from_attributes = True


class Transaction(TransactionBase, table=True):
    """Base table model for all financial transactions."""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    type: str = Field(index=True)  # 'income' or 'expense'


# Income model
class IncomeBase(TransactionBase):
    """Base model for income transactions."""
    origin: str = Field(index=True)


class IncomeCreate(IncomeBase):
    """Model for creating income transactions."""
    pass


class Income(IncomeBase, table=True):
    """Database model for income transactions."""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class IncomePublic(IncomeBase):
    """Public model for income transactions."""
    id: uuid.UUID


class IncomesPublic(SQLModel):
    """Response model for paginated income transactions."""
    data: list[IncomePublic]
    count: int
    pagination: dict[str, int] | None = None


# Expense model
class ExpenseBase(TransactionBase):
    """Base model for expense transactions."""
    category: str = Field(index=True)
    subcategory: str = Field(index=True)
    tags: str | None = Field(default=None, index=True)


class ExpenseCreate(ExpenseBase):
    """Model for creating expense transactions."""
    pass


class Expense(ExpenseBase, table=True):
    """Database model for expense transactions."""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class ExpensePublic(ExpenseBase):
    """Public model for expense transactions."""
    id: uuid.UUID


class ExpensesPublic(SQLModel):
    """Response model for paginated expense transactions."""
    data: list[ExpensePublic]
    count: int
    pagination: dict[str, int] | None = None

# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)
