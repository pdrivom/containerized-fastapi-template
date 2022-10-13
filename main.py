"""Main file for the Calendar API."""
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles

from db import database
from resources.routes import api_router

app = FastAPI(
    swagger_ui_parameters={"defaultModelsExpandDepth": 0},
    title="Calendar API",
    description="A Full-featured API for creating and managing a calendar.",
    redoc_url=None,
    docs_url=None,  # we customize this ourselves
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    contact={
        "name": "Grant Ramsay",
        "url": "https://www.gnramsay.com",
    },
)

app.include_router(api_router)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
async def startup():
    """Connect to the database on startup."""
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    """Disconnect from the database on shutdown."""
    await database.disconnect()


# --------------------- override the default Swagger docs -------------------- #
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    """Customize the default Swagger docs.

    In this case we merely override the default page title.
    """
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} | Documentation",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui.css",
    )
