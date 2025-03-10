from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Метод для хеширования пароля
    """

    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Метод для проверки пароля
    :param plain_password: str
    :param hashed_password: str
    :return: bool
    """

    return pwd_context.verify(plain_password, hashed_password)
