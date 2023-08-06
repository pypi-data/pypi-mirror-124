"""Quickly add RapiDoc to FastAPI"""

__version__ = '0.1.3'

from fastapi.responses import HTMLResponse
from fastapi import APIRouter


def get_router(*,
             openapi_url: str = "/openapi.json",
             title: str = "FastAPI",
             redoc_js_url: str = "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js",
             redoc_favicon_url: str = "https://fastapi.tiangolo.com/img/favicon.png",
             with_google_fonts: bool = True, ) -> APIRouter:
    router = APIRouter()

    @router.get("/rapidcoc")
    def get():
        html = f"""
            <!DOCTYPE html>
            <html>
            <head>
            <title>{title}</title>
            <!-- needed for adaptive design -->
            <meta charset="utf-8"/>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            """
        if with_google_fonts:
            html += """
            <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
            """
        html += f"""
            <link rel="shortcut icon" href="{redoc_favicon_url}">
            <!--
            ReDoc doesn't change outer page styles
            -->
            <style>
              body {{
                margin: 0;
                padding: 0;
              }}
            </style>
            </head>
            <body>
            <redoc spec-url="{openapi_url}"></redoc>
            <script src="{redoc_js_url}"> </script>
            </body>
            </html>
            """
        return HTMLResponse(html)

    return router
