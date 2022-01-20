from fastapi import APIRouter, Depends, HTTPException
from .views import ArtistView

from .service import get_artist_view
from ..dependencies import check_404, get_state, verify_token

artists = APIRouter(
    prefix="/artists",
    tags=["artists"],
    dependencies=[Depends(verify_token)],
    responses={404: {"description": "Not found"}},
)


@artists.get("/{id}", response_model=ArtistView)
async def artist(id: int, state=Depends(get_state)):
    response = get_artist_view(db_session=state.db, id=id)
    return check_404(response)
