from tests.helpers.api_client import ApiClient


class AuthManager:
    """
    Авторизация:
    - получение токена
    - хранение токена
    - добавление токена в заголовки
    """

    def __init__(self, api_client: ApiClient):
        self.api_client = api_client
        self._token: str | None = None

    @property
    def token(self) -> str | None:
        return self._token

    def login(self, username: str, password: str) -> str:
        response = self.api_client.post(
            "/auth/login/",
            data={"username": username, "password": password}
        )
        response.raise_for_status()
        data = response.json()
        self._token = data.get("access_token") or data.get("token")
        if not self._token:
            raise ValueError(f"Токен не найден в ответе: {data}")
        return self._token

    def register(self, username: str, password: str, email: str = None) -> dict:
        if email is None:
            email = f"{username}@test.com"
        response = self.api_client.post(
            "/auth/register/",
            data={
                "username": username,
                "password": password,
                "password_repeat": password,
                "email": email
            }
        )
        response.raise_for_status()
        return response.json()

    def get_auth_headers(self) -> dict:
        if not self._token:
            raise RuntimeError("Сначала выполните login()")
        return {"Authorization": f"Bearer {self._token}"}
