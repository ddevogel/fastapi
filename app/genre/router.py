from fastapi import APIRouter, Depends, HTTPException, Response
from .views import GenreView

from .service import get_genre_view, merge_genre
from ..dependencies import check_404, get_state, verify_token

genres = APIRouter(
    prefix="/genres",
    tags=["genres"],
    dependencies=[Depends(verify_token)],
    responses={404: {"description": "Not found"}},
)


@genres.get("/genre/{id}", response_model=GenreView)
async def genre(id: int, response: Response, state=Depends(get_state)):
    result = get_genre_view(db_session=state.db, id=id)
    response.headers["request_id"] = state.id
    return check_404(result)


@genres.put("/genre")
async def update_genre(genre: GenreView, state=Depends(get_state)):
    return merge_genre(db_session=state.db, genre=genre)