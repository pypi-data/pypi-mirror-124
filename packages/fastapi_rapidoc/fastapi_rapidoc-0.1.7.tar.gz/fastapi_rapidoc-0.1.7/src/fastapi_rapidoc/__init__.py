"""Quickly add RapiDoc to FastAPI"""

__version__ = "0.1.7"

from fastapi.responses import HTMLResponse
from fastapi import APIRouter


def get_router(
    *,
    openapi_url: str = "/openapi.json",
    title: str = "FastAPI",
    rapidoc_js_url: str = "https://unpkg.com/rapidoc/dist/rapidoc-min.js",
    rapidoc_favicon_url: str = "https://fastapi.tiangolo.com/img/favicon.png",
    with_google_fonts: bool = True,
) -> APIRouter:
    router = APIRouter()

    @router.get("/", include_in_schema=False)
    def get_rapidoc_html() -> HTMLResponse:
        html = f"""
        <!doctype html> <!-- Important: must specify -->
    <html>
    <head>
    <title>{title}</title>
      <meta charset="utf-8"> <!-- Important: rapi-doc uses utf8 charecters -->
      <script type="module" src="{rapidoc_js_url}"></script>
      <link rel="shortcut icon" href="{rapidoc_favicon_url}">
    </head>
    <body>
      <rapi-doc
        spec-url="{openapi_url}"
        theme="dark"
        load-fonts="{str(with_google_fonts).lower()}"
      > </rapi-doc>
    </body>
    </html>

        """
        return HTMLResponse(html)

    return router
