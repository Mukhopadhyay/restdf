import json
import pandas as pd
from schemas import request, response
from typing import Optional, List


class DataService:
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df

    @staticmethod
    def post_process(
        df: pd.DataFrame, type: str, columns: Optional[List[str]] = []
    ) -> dict:
        df: pd.DataFrame = df[columns] if columns else df
        return response.DataResponse(
            data=json.loads(df.to_json(orient="records")), type=type
        )

    def head(self, payload: request.HeadPayload) -> None:
        df: pd.DataFrame = self.df.head(n=payload.num)
        return self.post_process(df, type="head", columns=payload.columns)

    def sample(self, payload: request.SamplePayload) -> None:
        df: pd.DataFrame = self.df.sample(payload.num)
        return self.post_process(df, type="sample", columns=payload.columns)

    def equals(self, column, payload: request.ConditionalData) -> None:
        if payload.as_string:
            temp_df = self.df[self.df[column].astype(str) == payload.value]
        else:
            temp_df = self.df[self.df[column] == payload.value]

        return self.post_process(temp_df, type="equals", columns=payload.columns)

    def not_equals(self, column, payload: request.ConditionalData) -> None:
        if payload.as_string:
            temp_df = self.df[self.df[column].astype(str) == payload.value]
        else:
            temp_df = self.df[self.df[column] != payload.value]

        return self.post_process(temp_df, type="not_equals", columns=payload.columns)

    def isin(self, column, payload: request.MultiConditionalData) -> None:
        if payload.as_string:
            temp_df = self.df[self.df[column].astype(str).isin(payload.values)]
        else:
            temp_df = self.df[self.df[column].isin(payload.values)]

        return self.post_process(temp_df, type="isin", columns=payload.columns)

    def notin(self, column, payload: request.MultiConditionalData) -> None:
        if payload.as_string:
            temp_df = self.df[~self.df[column].astype(str).isin(payload.values)]
        else:
            temp_df = self.df[~self.df[column].isin(payload.values)]

        return self.post_process(temp_df, type="notin", columns=payload.columns)

    def str_contains(self, column, payload: request.FindStringData) -> None:
        kwargs = dict(
            pat=payload.pattern,
            case=payload.case,
            flags=payload.flags,
            na=payload.na,
            regex=payload.regex,
        )
        temp_df = self.df[self.df[column].str.contains(**kwargs)]

        return self.post_process(temp_df, type="str_contains", columns=payload.columns)
