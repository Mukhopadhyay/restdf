"""
Data Controller
"""

import enum
from typing import List

import pandas as pd
from fastapi import APIRouter
from typing import Optional


from schemas import request, response
from modules.data.service import DataService


class DataController:
    def __init__(
        self,
        df: pd.DataFrame,
        prefix: Optional[str] = "/data",
        tags: Optional[List[str]] = ["Data"],
        name: Optional[str] = "RestDF",
    ) -> None:
        self.__df: pd.DataFrame = df
        self.__router: APIRouter = None
        self.Columns = enum.Enum("Columns", {x: x for x in self.__df.columns})

        self.prefix = prefix
        if not self.prefix:
            self.prefix = ""

        self.tags = tags
        if not self.tags:
            self.tags = []

        self.name = name
        if not self.name:
            self.name = self.NAME

    def generate(self) -> None:
        """
        Generates the APIRouter
        """

        # self.__router = APIRouter(prefix="/restdf/data", tags=self.TAGS)
        self.__router = APIRouter(prefix=self.prefix, tags=self.tags)

        @self.__router.post("/head", response_model=response.DataResponse)
        async def head(data: request.DataRequest):
            """
            **Returns the head of the dataframe.**

            This endpoint returns the response from <code>df.head()</code> & returns the result.
            """
            service = DataService(self.__df)
            return service.head(data)

        @self.__router.post("/sample", response_model=response.DataResponse)
        async def sample(data: request.SamplePayload):
            """
            **Returns random rows from the dataframe.**

            This endpoint returns the response from <code>df.sample(**kwargs)</code> & returns the result.

            **num**: int: _OPTIONAL_ - Number of items from axis to return. Cannot be used with frac. Default = 1 if frac = None

            **frac**: float: _OPTIONA                                                                                               L_ - Fraction of axis items to return. Cannot be used with n.

            **weights**: str or list: _OPTIONAL_ - Default 'None' results in equal probability weighting.

            **random_state**: int: _OPTIONAL_ - Given int will be used as a seed for random number generator.

            **axis**: int: _OPTIONAL) - 0 or 'index', 1 or 'columns', Defaults to None

            **ignore_index**: bool: _OPTIONAL_ - If True, the resulting index will be labeled 0, 1, ..., n-1

            """
            service = DataService(self.__df)
            return service.sample(data)

        @self.__router.post("/equals/{column}", response_model=response.DataResponse)
        async def equals(column: self.Columns, data: request.ConditionalData):
            """
            **Returns rows where all column values are exactly equal to the given value**

            For the given column name, this endpoint returns the rows where the values for that column is equal to <code>value</code>.
            """
            service = DataService(self.__df)
            return service.equals(column.value, data)

        @self.__router.post(
            "/not_equals/{column}", response_model=response.DataResponse
        )
        async def not_equals(column: self.Columns, data: request.ConditionalData):
            """
            **Returns rows where all column values are not equal to the given value**

            For the given column name, this endpoint returns the rows where the values for that column is not equal to <code>value</code>.
            """
            service = DataService(self.__df)
            return service.not_equals(column.value, data)

        @self.__router.post("/isin/{column}", response_model=response.DataResponse)
        async def isin(column: self.Columns, data: request.MultiConditionalData):
            """
            **Returns rows where all column values are within the array content**

            For the given column name, this endpoint returns the rows where the values are within the <code>values</code> array
            """
            service = DataService(self.__df)
            return service.isin(column.value, data)

        @self.__router.post("/notin/{column}", response_model=response.DataResponse)
        async def notin(column: self.Columns, data: request.MultiConditionalData):
            """
            **Returns rows where all column values are not within the array content**

            For the given column name, this endpoint returns the rows where the values are not within the <code>values</code> array. Basically, the inverse of <code>/isin</code> endpoint.
            """
            service = DataService(self.__df)
            return service.notin(column.value, data)

        @self.__router.post(
            "/str_contains/{column}", response_model=response.DataResponse
        )
        async def str_contains(column: self.Columns, data: request.FindStringData):
            """
            **Returns rows where all string values contains given pattern**

            For the given column name, this endpoint returns the rows where the values (string DataTypes) for that column containg the given
            pattern. This uses the <code>str.contains()</code> method, please refer to
            <a href='https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.str.contains.html'
            target='_blank'>this</a> page for more details.
            """
            service = DataService(self.__df)
            return service.str_contains(column.value, data)

    def get_router(self) -> APIRouter:
        """
        Returns the generated APIRouter.
        """
        return self.__router
