from pydantic import BaseModel, ConfigDict


class MovieBase(BaseModel):
    title: str
    release_year: int
    genre: str
    producer: str | None = None
    duration: int
    actors: str


class MovieCreate(MovieBase):
    pass


class MovieUpdate(BaseModel):
    title: str | None = None
    release_year: int | None = None
    genre: str | None = None
    producer: str | None = None
    duration: int | None = None
    actors: str | None = None


class MovieResponse(MovieBase):
    id: int

    model_config = ConfigDict(from_attributes=True)