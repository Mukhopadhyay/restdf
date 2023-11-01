"""
Data Controller
"""

import enum
from typing import List

import pandas as pd
from fastapi import APIRouter

from schemas import request, response
from modules.data.service import DataService


class DataController:
    TAGS: List[str] = ["Data"]

    def __init__(self, df: pd.DataFrame) -> None:
        self.__df: pd.DataFrame = df
        self.__router: APIRouter = None
        self.Columns = enum.Enum("Columns", {x: x for x in self.__df.columns})

    def generate(self) -> None:
        """
        Generates the APIRouter
        """

        self.__router = APIRouter(prefix="/data", tags=self.TAGS)

        @self.__router.post("/head")
        async def head(data: request.HeadPayload):
            """
            **Returns the head of the dataframe.**

            This endpoint returns the response from <code>df.head()</code> & returns the result.
            """
            service = DataService(self.__df)
            return service.head(data)

        @self.__router.post("/sample")
        async def sample(data: request.SamplePayload):
            """
            **Returns random rows from the dataframe.**

            This endpoint returns the response from <code>df.sample(**kwargs)</code> & returns the result.
            """
            service = DataService(self.__df)
            return service.sample(data)

        @self.__router.post("/equals/{column}")
        async def equals(column: self.Columns, data: request.ConditionalData):
            """
            **Returns rows where all column values are exactly equal to the given value**

            For the given column name, this endpoint returns the rows where the values for that column is equal to <code>value</code>.
            """
            service = DataService(self.__df)
            return service.equals(column.value, data)

        @self.__router.post("/not_equals/{column}")
        async def not_equals(column: self.Columns, data: request.ConditionalData):
            service = DataService(self.__df)
            return service.not_equals(column.value, data)

        @self.__router.post("/isin/{column}")
        async def isin(column: self.Columns, data: request.MultiConditionalData):
            service = DataService(self.__df)
            return service.isin(column.value, data)

        @self.__router.post("/notin/{column}")
        async def notin(column: self.Columns, data: request.MultiConditionalData):
            service = DataService(self.__df)
            return service.notin(column.value, data)

        @self.__router.post("/str_contains/{column}")
        async def str_contains(column: self.Columns, data: request.FindStringData):
            service = DataService(self.__df)
            return service.str_contains(column.value, data)

    def get_router(self) -> APIRouter:
        return self.__router
