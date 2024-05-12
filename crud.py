import asyncio

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, User, Profile, Post


async def create_user(session: AsyncSession, username: str) -> User:
    user = User(user_name=username)
    session.add(user)
    await session.commit()
    print(f"{user=}")
    return user


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    smtp = select(User).where(User.user_name == username)
    # result: Result = await session.execute(smtp)
    # user: User | None = result.scalar_one_or_none()  # строго один пользователь или None
    # user: User = result.scalar_one()  # строго один пользователь или ошибка
    user: User | None = await session.scalar(smtp)
    print("Found user:", username, user)
    return user


async def create_user_profile(
    session: AsyncSession,
    user_id: int,
    first_name: str | None = None,
    last_name: str | None = None,
) -> Profile:
    profile = Profile(user_id=user_id, first_name=first_name, last_name=last_name)
    session.add(profile)
    await session.commit()
    return profile


async def show_users_with_profile(session: AsyncSession):
    smtp = select(User).options(joinedload(User.profile)).order_by(User.id)

    # result: Result = await session.execute(smtp)
    # users = result.scalars()
    users = await session.scalars(smtp)

    for user in users:
        print(user)
        print(user.profile.first_name)

    # return users


async def create_posts(
    session: AsyncSession, user_id: int, *post_titles: str
) -> list[Post]:
    posts = [Post(title=title, user_id=user_id) for title in post_titles]
    session.add_all(posts)
    await session.commit()
    print(posts)
    return posts


async def get_users_with_posts(session: AsyncSession):
    smtp = select(User).options(joinedload(User.posts)).order_by(User.id)
    users = await session.scalars(smtp)

    for user in users.unique():
        print("**" * 10)
        print(user)
        for post in user.posts:
            print(" - ", post)


async def get_users_with_posts_result(session: AsyncSession):
    """
    Под капотом использует inner join и надо еще уникализировать коллекцию
    :param session:
    :return:
    """
    smtp = select(User).options(joinedload(User.posts)).order_by(User.id)
    result: Result = await session.execute(smtp)
    users = result.unique().scalars()

    for user in users:
        print("**" * 10)
        print(user)
        for post in user.posts:
            print(" - ", post)


async def get_users_with_posts_select_in_load(session: AsyncSession):
    """
    Работает как жадная загрузка в Laravel
    :param session:
    :return:
    """
    smtp = select(User).options(selectinload(User.posts)).order_by(User.id)
    result: Result = await session.execute(smtp)
    users = result.scalars()

    for user in users:
        print("**" * 10)
        print(user)
        for post in user.posts:
            print(" - ", post)


async def get_post_with_author(session: AsyncSession):
    stmt = select(Post).options(joinedload(Post.user)).order_by(Post.id)
    posts = await session.scalars(stmt)

    for post in posts:  # type: Post
        print("**" * 10)
        print("Post:", post)
        print("Author:", post.user)


async def get_users_with_posts_and_profiles(session: AsyncSession):
    smtp = (
        select(User)
        .options(joinedload(User.profile), selectinload(User.posts))
        .order_by(User.id)
    )

    users = await session.scalars(smtp)

    for user in users:  # type: User
        print("**" * 10)
        print(user, user.profile and user.profile.first_name)
        for post in user.posts:
            print(" - ", post)


async def get_profile_with_users_and_with_post(session: AsyncSession):
    stmt = (
        select(Profile)
            # .join(Profile.user)
            .options(joinedload(Profile.user).selectinload(User.posts))
            .where(User.user_name == "John")
            .order_by(Profile.id)
    )
    profiles = await session.scalars(stmt)

    for profile in profiles:  # type: Profile
        print("**" * 10)
        print(profile.first_name, profile.user)
        print(profile.user.posts)


async def main():
    async with db_helper.session_factory() as session:
        # await create_user(session=session, username="Alice")
        # await create_user(session=session, username="Sam")
        # user_sam = await get_user_by_username(session=session, username="Sam")
        # # await get_user_by_username(session=session, username="Bob")
        # user_john = await get_user_by_username(session=session, username="John")
        #
        # user_john_inf = await create_user_profile(session=session, user_id=user_john.id, first_name=user_john.user_name, last_name="Jonsonjuk")
        # user_sam_inf = await create_user_profile(session=session, user_id=user_sam.id, first_name=user_sam.user_name, last_name="White")
        # print(user_john_inf)
        # await show_users_with_profile(session=session)
        # await create_posts(session, user_john.id, "SQLA 2.0", "SQLA Joins")
        # await create_posts(session, user_sam.id, "Fast API Intro", "Fast API Advanced", "Fast API more")

        #
        # await get_users_with_posts(session=session)
        # await get_users_with_posts_result(session=session)
        # await get_users_with_posts_select_in_load(session=session)

        # await get_post_with_author(session=session)

        # await get_users_with_posts_and_profiles(session=session)

        await get_profile_with_users_and_with_post(session=session)


if __name__ == "__main__":
    asyncio.run(main())
