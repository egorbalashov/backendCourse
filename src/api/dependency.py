

from typing import Annotated
from fastapi import Depends, Query
from pydantic import BaseModel


class PaginationParams(BaseModel):

    page: Annotated[int, Query(1, ge=1, description="Номер страницы")] 
    per_page: Annotated[int, Query(2, gt=1, lt=30, description="Количество элементов на странице")] 


PaginationDep = Annotated[PaginationParams, Depends()]
