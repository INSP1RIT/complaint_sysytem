from typing import Optional, List

from fastapi import APIRouter, Depends

from managers.auth import oauth2_scheme, is_admin
from managers.user import UserManager
from schemas.response.user import UserOut

router = APIRouter(tags=['users'])


@router.get("/users/", dependencies=[Depends(oauth2_scheme), Depends(is_admin)], response_model=List[UserOut])
async def get_users(email: Optional[str] = None):
    if email:
        return await UserManager.get_user_by_email(email)

    return await UserManager.get_all_users()
