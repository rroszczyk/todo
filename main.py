from typing import Optional

import fastapi
import uvicorn

import logging
import graypy

logger = logging.getLogger()

handler = graypy.GELFTLSHandler('dione', 12201)
logger.addHandler(handler)

api = fastapi.FastAPI()

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
    try:
        value = x / y
    except ZeroDivisionError:
        return fastapi.responses.HTMLResponse(
            content="<html><body>Błąd dzielenia przez zero</body></html>",
            status_code=400
        )

    if z is not None:
        z = z ** 2

    return {
        'x': x,
        'y': y,
        'z': z,
        'value': value
    }

if __name__ == '__main__':
    uvicorn.run(api, port=8000, host="127.0.0.1")

