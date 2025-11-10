"""Example CRUD operations using the fastapi-base-crud library."""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path to import crud module
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from crud.base import CRUDBase
from crud.iao.base import CRUDBase as AsyncCRUDBase
from example.db import get_db, get_db_async
from example.models import User
from example.schemas import UserFilter, UserInput, UserUpdateInput


# Synchronous example
def test_sync_crud():
    """Test synchronous CRUD operations."""
    db = next(get_db())

    user_crud = CRUDBase[User, UserInput, UserUpdateInput, UserFilter](db, "id")

    # Create
    print("=" * 60)
    print("SYNCHRONOUS CRUD OPERATIONS")
    print("=" * 60)

    user = user_crud.create(
        UserInput(
            username="johndoe",
            email="john.doe@example.com",
            full_name="John Doe",
            bio="Software developer",
        )
    )
    print(f"\n✓ Created user: {user}")
    user_id = user.id

    # Read by ID
    user_from_db = user_crud.read_by_id(user_id)
    print(f"\n✓ Read user by ID: {user_from_db}")

    # Read all
    users = user_crud.read()
    print(f"\n✓ Read all users: {len(users)} user(s) found")

    # Read with filter
    active_users = user_crud.read(read_schema=UserFilter(is_active=True))
    print(f"\n✓ Read active users: {len(active_users)} active user(s)")

    # Update
    updated_user = user_crud.update(
        user_id, UserUpdateInput(bio="Senior Software Developer")
    )
    print(f"\n✓ Updated user: {updated_user} row(s) affected")

    # Read updated user
    updated_user_from_db = user_crud.read_by_id(user_id)
    print(f"\n✓ User after update: {updated_user_from_db}")

    # Delete
    deleted_user = user_crud.delete(user_id)
    print(f"\n✓ Deleted user: {deleted_user}")

    # Verify deletion
    deleted_check = user_crud.read_by_id(user_id)
    print(f"\n✓ User after deletion: {deleted_check}")


# Asynchronous example
async def test_async_crud():
    """Test asynchronous CRUD operations."""
    async_db_gen = get_db_async()
    async_db = await anext(async_db_gen)

    async_user_crud = AsyncCRUDBase[User, UserInput, UserUpdateInput, UserFilter](
        async_db, "id"
    )

    # Create
    print("\n" + "=" * 60)
    print("ASYNCHRONOUS CRUD OPERATIONS")
    print("=" * 60)

    async_user = await async_user_crud.create(
        UserInput(
            username="janedoe",
            email="jane.doe@example.com",
            full_name="Jane Doe",
            bio="Data scientist",
        )
    )
    print(f"\n✓ Created user: {async_user}")
    async_user_id = async_user.id

    # Read by ID
    async_user_from_db = await async_user_crud.read_by_id(async_user_id)
    print(f"\n✓ Read user by ID: {async_user_from_db}")

    # Read all
    async_users = await async_user_crud.read()
    print(f"\n✓ Read all users: {len(async_users)} user(s) found")

    # Read with pagination and filter
    async_users_paginated = await async_user_crud.read(
        limit=10, offset=0, read_schema=UserFilter(username="janedoe")
    )
    print(f"\n✓ Read users (paginated, filtered): {len(async_users_paginated)} user(s)")

    # Update
    async_updated_user = await async_user_crud.update(
        async_user_id,
        UserUpdateInput(bio="Senior Data Scientist", full_name="Jane M. Doe"),
    )
    print(f"\n✓ Updated user: {async_updated_user} row(s) affected")

    # Read updated user
    async_updated_user_from_db = await async_user_crud.read_by_id(async_user_id)
    print(f"\n✓ User after update: {async_updated_user_from_db}")

    # Delete
    async_deleted_user = await async_user_crud.delete(async_user_id)
    print(f"\n✓ Deleted user: {async_deleted_user}")

    # Verify deletion
    async_deleted_check = await async_user_crud.read_by_id(async_user_id)
    print(f"\n✓ User after deletion: {async_deleted_check}")


# Run examples
if __name__ == "__main__":
    # Windows compatibility: use SelectorEventLoop instead of ProactorEventLoop
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    print("\n" + "=" * 60)
    print("FASTAPI-BASE-CRUD EXAMPLE")
    print("=" * 60)

    # Run synchronous example
    test_sync_crud()

    # Run asynchronous example
    asyncio.run(test_async_crud())

    print("\n" + "=" * 60)
    print("EXAMPLES COMPLETED")
    print("=" * 60 + "\n")
