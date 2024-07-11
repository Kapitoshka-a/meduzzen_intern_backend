from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_async_session
from app.schemas.user_schemas import *
from app.services.user_crud import UserCRUD

from app.utils.exception_handler import handle_exceptions
from fastapi_pagination import LimitOffsetPage, add_pagination


router = APIRouter(
    prefix="/api/users", tags=["Users"], dependencies=[Depends(handle_exceptions)]
)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=LimitOffsetPage[UserBriefResponseSchema]
)
async def get_users(session: AsyncSession = Depends(get_async_session)):
    user_crud = UserCRUD(session)
    users = await user_crud.get_all_users()
    return users


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_user(
        user: SignInRequestSchema, session: AsyncSession = Depends(get_async_session)
):
    user_crud = UserCRUD(session)
    return await user_crud.create_user(user)


@router.get(
    "/{user_id}",
    response_model=UserDetailResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def get_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    user_crud = UserCRUD(session)
    user = await user_crud.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put(
    "/{user_id}",
    response_model=UserDetailResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def update_user(
        user_id: int,
        user_update: UserUpdateRequestSchema,
        session: AsyncSession = Depends(get_async_session),
):
    user_crud = UserCRUD(session)
    db_user = await user_crud.update_user(user_id, user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    user_crud = UserCRUD(session)
    if not await user_crud.delete_user(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return
