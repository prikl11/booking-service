from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.database.db import get_db


SessionDep = Annotated[AsyncSession, Depends(get_db)]