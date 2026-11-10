from typing import Annotated  # Annotated — для Form() і Cookie()

from fastapi import (
    APIRouter,
    Cookie,  # Cookie — читання cookie із запиту
    Form,  # Form — читання полів HTML-форми (потрібен python-multipart)
    HTTPException,  # HTTPException — відповіді з кодами помилок
    Response,  # Response — через нього ставимо/видаляємо cookie
)

from app import session_store  # створення/видалення сесій
from app.config import settings  # налаштування cookie
from app.database import DbSession  # сеанс БД
from app.dependencies import CurrentUser  # поточний користувач (захист маршруту)
from app.services import user_service  # робота з користувачами

# prefix — спільний початок шляхів; tags — групування в документації /docs.
router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=201)
def register(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    db: DbSession,
):
    """Реєстрація: створює користувача (пароль зберігається лише як хеш)."""
    if user_service.get_by_username(db, username) is not None:
        raise HTTPException(status_code=400, detail="Користувач уже існує")
    user = user_service.create_user(db, username, password)
    return {"id": user.id, "username": user.username}


@router.post("/login")
def login(
    response: Response,
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    db: DbSession,
):
    """Вхід: перевірка пароля -> нова сесія -> cookie з session_id."""
    user = user_service.authenticate(db, username, password)
    if user is None:
        # Однакове повідомлення і для «немає логіна», і для «хибний пароль».
        raise HTTPException(status_code=401, detail="Невірний логін або пароль")

    session_id = session_store.create_session(user.id)
    response.set_cookie(
        key=settings.cookie_name,
        value=session_id,
        httponly=True,  # JavaScript не може прочитати cookie
        secure=settings.cookie_secure,  # лише HTTPS (у production)
        samesite="lax",  # обмеження міжсайтових запитів
        max_age=settings.cookie_max_age,  # скільки живе cookie в браузері
    )
    return {"message": "Вхід виконано"}


@router.get("/me")
def me(user: CurrentUser):
    """Відновлення сесії: хто зараз увійшов (потрібна чинна cookie)."""
    return {"id": user.id, "username": user.username}


@router.post("/logout")
def logout(
    response: Response,
    session_id: Annotated[str | None, Cookie()] = None,
):
    """Вихід: видаляємо сесію НА СЕРВЕРІ і просимо браузер стерти cookie."""
    session_store.delete_session(session_id)
    response.delete_cookie(settings.cookie_name)
    return {"message": "Вихід виконано"}
