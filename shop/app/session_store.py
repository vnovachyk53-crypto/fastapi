import secrets  # secrets — криптографічно стійкі випадкові значення

# session_id -> id користувача
_sessions: dict[str, int] = {}


def create_session(user_id: int) -> str:
    """Створити сесію й повернути її ідентифікатор."""
    # token_urlsafe(32): 32 випадкові байти (256 біт), рядок із 43 символів.
    session_id = secrets.token_urlsafe(32)
    _sessions[session_id] = user_id
    return session_id


def get_user_id(session_id: str | None) -> int | None:
    """За ідентифікатором знайти id користувача (або None)."""
    if not session_id:
        return None
    return _sessions.get(session_id)


def delete_session(session_id: str | None) -> None:
    """Видалити сесію (вихід). Якщо її немає — нічого не робимо."""
    if session_id:
        _sessions.pop(session_id, None)
