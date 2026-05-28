import requests
from tests.utils.logger import Logger


class ApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

    def _build_url(self, path: str) -> str:
        return f"{self.base_url}/{path.lstrip('/')}"

    def get(self, path: str, headers: dict = None, params: dict = None) -> requests.Response:
        url = self._build_url(path)
        Logger.debug(f"GET {url}")
        response = self.session.get(url, headers=headers, params=params)
        Logger.debug(f"Response {response.status_code}: {response.text[:200]}")
        return response

    def post(self, path: str, json_data: dict = None, data: dict = None, headers: dict = None) -> requests.Response:
        url = self._build_url(path)
        Logger.debug(f"POST {url} | json={json_data} | data={data}")
        response = self.session.post(url, json=json_data, data=data, headers=headers)
        Logger.debug(f"Response {response.status_code}: {response.text[:200]}")
        return response

    def put(self, path: str, json_data: dict = None, data: dict = None, headers: dict = None) -> requests.Response:
        url = self._build_url(path)
        Logger.debug(f"PUT {url} | json={json_data} | data={data}")
        response = self.session.put(url, json=json_data, data=data, headers=headers)
        Logger.debug(f"Response {response.status_code}: {response.text[:200]}")
        return response

    def delete(self, path: str, headers: dict = None) -> requests.Response:
        url = self._build_url(path)
        Logger.debug(f"DELETE {url}")
        response = self.session.delete(url, headers=headers)
        Logger.debug(f"Response {response.status_code}: {response.text[:200]}")
        return response
