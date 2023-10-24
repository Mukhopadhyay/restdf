import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from api import router

app = FastAPI()

app.include_router(router)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="filename.csv",
        version="1.0.0",
        # summary="Created using <a href='https://github.com/Mukhopadhyay/restdf'>RestDF</a>",
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


# Main method
def main() -> None:
    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info")


if __name__ == "__main__":
    main()
