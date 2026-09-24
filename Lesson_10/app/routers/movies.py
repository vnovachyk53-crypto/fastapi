from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError
from .. import schemas
from ..dependencies import SessionDep
from ..services import movie_service

router = APIRouter(prefix="/movies", tags=["movies"])


@router.post(
    "/",
    response_model=schemas.MovieResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_movie(payload: schemas.MovieCreate, db: SessionDep):
    try:
        return movie_service.create_movie(db, payload)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Could not create movie",
        )


@router.get("/", response_model=list[schemas.MovieResponse])
def read_movies(
    db: SessionDep,
    genre: str | None = None,
    release_year: int | None = None,
    limit: int = 20,
    offset: int = 0,
):
    return movie_service.get_movies(db, genre, release_year, limit, offset)


@router.get("/{movie_id}", response_model=schemas.MovieResponse)
def read_movie(movie_id: int, db: SessionDep):
    movie = movie_service.get_movie(db, movie_id)
    if movie is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found",
        )
    return movie


@router.patch("/{movie_id}", response_model=schemas.MovieResponse)
def update_movie(movie_id: int, payload: schemas.MovieUpdate, db: SessionDep):
    movie = movie_service.get_movie(db, movie_id)
    if movie is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found",
        )
    try:
        return movie_service.update_movie(db, movie, payload)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Could not update movie",
        )


@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(movie_id: int, db: SessionDep):
    movie = movie_service.get_movie(db, movie_id)
    if movie is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found",
        )
    movie_service.delete_movie(db, movie)