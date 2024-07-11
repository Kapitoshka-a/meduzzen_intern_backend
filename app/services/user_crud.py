from typing import List

from fastapi import HTTPException
from fastapi_pagination import LimitOffsetPage, pagination_ctx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.user_models import UserModel
from app.schemas.user_schemas import (
    SignInRequestSchema,
    UserDetailResponseSchema,
    UserBriefResponseSchema,
    UserUpdateRequestSchema,
    UsersListResponseSchema,
)
from app.core.hashing import hashed_password
from fastapi_pagination.ext.sqlalchemy import paginate


class UserCRUD:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(self, user: SignInRequestSchema) -> UserDetailResponseSchema:
        if user.email:
            existing_user = await self.get_user_by_email(user.email)
            if existing_user:
                raise HTTPException(status_code=400, detail="Email already registered")
        db_user = UserModel(
            firstname=user.firstname,
            lastname=user.lastname,
            email=user.email,
            hashed_password=hashed_password(user.password1),
            avatar=user.avatar,
            city=user.city,
            phone=user.phone,
        )
        self.db_session.add(db_user)
        await self.db_session.commit()
        await self.db_session.refresh(db_user)
        return UserDetailResponseSchema.from_orm(db_user)

    async def get_user_by_id(self, user_id: int) -> UserDetailResponseSchema | None:
        result = await self.db_session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        return result.scalars().first()

    async def get_user_by_email(self, user_email: str):
        result = await self.db_session.execute(
            select(UserModel).filter(UserModel.email == user_email)
        )
        return result.scalars().first()

    async def get_all_users(self) -> LimitOffsetPage[UserBriefResponseSchema]:
        query = select(UserModel).order_by(UserModel.created_at)
        paginated_users = await paginate(self.db_session, query)
        items = [UserBriefResponseSchema.model_validate(user) for user in paginated_users.items]
        return LimitOffsetPage(
            items=items,
            total=paginated_users.total,
            limit=paginated_users.limit,
            offset=paginated_users.offset
        )

    async def update_user(
        self, user_id: int, user_update: UserUpdateRequestSchema
    ) -> UserDetailResponseSchema | None:
        db_user = await self.get_user_by_id(user_id)
        if db_user:
            update_data = user_update.model_dump(exclude_unset=True)
            new_hashed_password = hashed_password(update_data["password"])
            update_data.pop("password")
            update_data["hashed_password"] = new_hashed_password
            for key, value in update_data.items():
                setattr(db_user, key, value)
            await self.db_session.commit()
            await self.db_session.refresh(db_user)
            return db_user
        return None

    async def delete_user(self, user_id: int) -> bool:
        db_user = await self.get_user_by_id(user_id)
        if db_user:
            await self.db_session.delete(db_user)
            await self.db_session.commit()
            return True
        return False
