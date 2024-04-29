from backend.app.models import User, Role
from backend.app.databases.mysql import async_session, get_db_url, create_engine_and_session
from sqlalchemy import Select, select, update, desc, and_
from sqlalchemy.orm import selectinload, joinedload
import asyncio

async def async_main():
    user_id=6
    async with async_session() as db:
        r = await db.execute(
            select(User)
            .options(selectinload(User.dept))
            .options(selectinload(User.roles).joinedload(Role.menus))
            .where(User.id == user_id)
        )
        user = r.scalars().first()

        print(user.dept)

def main():
    user_id=6
    engine, session =  create_engine_and_session(get_db_url(False), False)
    with session() as db:
        r = db.begin.execute(
            select(User)
            .options(selectinload(User.dept))
            .options(selectinload(User.roles).joinedload(Role.menus))
            .where(User.id == user_id)
        )
        user = r.scalars().first()

        print(user.dept.users)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_main())
    # main()
