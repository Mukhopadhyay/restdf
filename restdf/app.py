import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware

from api import router as index_router

from api.data import DataController
from api.metadata import get_router as get_metadata_router

import pandas as pd

df = pd.read_csv("./../tests/test_data/test.csv")

app = FastAPI()

app.include_router(index_router, include_in_schema=False)

# Adding the routers

data_controller = DataController(df)
data_controller.generate()
app.include_router(data_controller.get_router())


# Cusomizing OpenAPI
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="filename.csv",
        version="1.0.0",
        description="""
Created using **[RestDF](https://github.com/Mukhopadhyay/restdf)**

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
        """,
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


# CORS (Cross-Origin-Resource-Sharing)
origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Main method
def main() -> None:
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")


if __name__ == "__main__":
    main()
