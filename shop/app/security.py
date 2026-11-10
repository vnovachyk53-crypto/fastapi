from pwdlib import (
    PasswordHash,  # PasswordHash — сучасне хешування паролів (за замовчуванням Argon2)
)

# recommended() — рекомендовані налаштування бібліотеки (Argon2).
password_hasher = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Пароль -> хеш (щоразу інший завдяки випадковій «солі»)."""
    return password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """Перевірка введеного пароля проти хеша з бази."""
    return password_hasher.verify(password, password_hash)
