from fastapi import FastAPI, Header, HTTPException
# Depends,
from service.artist_service import ArtistService
from service.employee_service import EmployeeService
from service.genre_service import GenreService
# from service.security_service import Token
from data.view_models import ArtistView, EmployeeView, GenreView
# from pydantic import *

# uvicorn main:app --reload --port 8001
app = FastAPI()

artist_service = ArtistService()
employee_service = EmployeeService()
genre_service = GenreService()


def __safe_get(value):
    if(value is None):
        raise HTTPException(status_code=404)
    return value


async def verify_token(xy_token: str = Header(...)):
    if xy_token != "secret":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


@app.get("/employee/{id}", response_model=EmployeeView)
async def employee(id: int):
    return __safe_get(employee_service.get_employee_view(id))


# dependencies=[Depends(verify_token)]
@app.get("/artist/{id}", response_model=ArtistView)
async def artist(id: int):
    return __safe_get(artist_service.get_artist_view(id))


@app.get("/genre/{id}", response_model=GenreView)
async def genre(id: int):
    return genre_service.get_genre_view(id)


@app.put("/genre")
async def update_genre(genre: GenreView):
    return __safe_get(genre_service.update_genre(genre))
