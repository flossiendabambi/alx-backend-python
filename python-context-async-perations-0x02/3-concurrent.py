#!/usr/bin/env python3
"""
Run multiple SQLite queries concurrently using aiosqlite and asyncio.gather.
"""

import asyncio
import aiosqlite


async def async_fetch_users():
    async with aiosqlite.connect("my_database.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            print("All users:")
            for user in users:
                print(user)
            return users


async def async_fetch_older_users():
    async with aiosqlite.connect("my_database.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            older_users = await cursor.fetchall()
            print("Users older than 40:")
            for user in older_users:
                print(user)
            return older_users


async def fetch_concurrently():
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )


if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
