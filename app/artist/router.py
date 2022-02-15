from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.security import SecurityScopes

from ..auth.service import get_current_user
from ..auth.views import User
from ..dependencies import check_404, get_state
from .service import get_artist_view
from .views import ArtistView

artists = APIRouter(
    prefix="/artists",
    tags=["artists"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@artists.get("/{id}", response_model=ArtistView)
async def artist(
    id: int,
    state=Depends(get_state),
    user=Security(get_current_user, scopes=["artist_read"]),
):
    response = get_artist_view(db_session=state.db, id=id)
    return check_404(response)
