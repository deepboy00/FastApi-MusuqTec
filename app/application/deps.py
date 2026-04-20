from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import decode_access_token
from app.infrastructure.db.repositories.admin_repo import AdminRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def get_current_admin(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No autenticado o token inválido",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    admin_id: int | None = payload.get("sub")
    if admin_id is None:
        raise credentials_exception

    repo = AdminRepository(db)
    admin = await repo.get_by_id(int(admin_id))
    if admin is None:
        raise credentials_exception

    return {"id": admin.id, "username": admin.username}
