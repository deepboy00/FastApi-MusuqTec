from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.schemas.auth_schema import TokenOut
from app.core.database import get_db
from app.core.security import create_access_token, verify_password
from app.infrastructure.db.repositories.admin_repo import AdminRepository

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=TokenOut)
async def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TokenOut:
    repo = AdminRepository(db)
    admin = await repo.get_by_username(form.username)

    if not admin or not verify_password(form.password, admin.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token({"sub": str(admin.id)})
    return TokenOut(access_token=token)
