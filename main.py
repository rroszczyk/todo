from typing import Optional

import fastapi
from fastapi.openapi.utils import get_openapi
import uvicorn

import logging
import graypy

# uruchomienie i konfiguracja logera z użyciem graylog
from views.user_views import user_router

logger = logging.getLogger()

handler = graypy.GELFTLSHandler('dione', 12201)

logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

def custom_openapi():
    '''
    Konfiguracja openAPI (www.swager.io)
    '''
    if api.openapi_schema:
        return api.openapi_schema

    openapi_schema = get_openapi(
        title="Nasza aplikacja TODO",
        version="1.0.0",
        description="To będzie API dla aplikacji TODO",
        routes=api.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    api.openapi_schema = openapi_schema
    return api.openapi_schema

# uruchomienie i konfiguracja silnika api
api = fastapi.FastAPI()
api.openapi = custom_openapi

api.include_router(user_router, prefix="/users")

# api.router.prefix = "/api/v1"

@api.get("/")
def index():
    body = """
    <html>
    <body>
    <h1>Witaj świecie z pierwszej aplikacji webowej napisanej w języku Python</h1>
    <a href='/calculate?x=10&y=15'>Test kalkulatora</a>
    <a href='/calculate?x=10&y=0'>Test błędu kalkulatora</a>
    <a href='/calculate?x=10&y=15&z=5'>Test kalkulatora</a>        
    </body>
    </html>
    """
    return fastapi.responses.HTMLResponse(content=body)

@api.get("/calculate")
def calculate(x: int, y: int, z: Optional[int] = None):
    '''
    Kalkulator liczący wynik z dzielenia x przez y
    '''
    try:
        value = x / y
    except ZeroDivisionError:
        return fastapi.responses.HTMLResponse(
            content="<html><body>Błąd dzielenia przez zero</body></html>",
            status_code=400
        )

    if z is not None:
        z = z ** 2

    logger.info("Wykonane zostały obliczenia w metodzie calculate")

    return {
        'x': x,
        'y': y,
        'z': z,
        'value': value
    }

if __name__ == '__main__':
    uvicorn.run(api, port=8000, host="127.0.0.1")

