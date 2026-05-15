import requests
from requests import Response


class BaseAPIClient:
    base_url: str

    def __init__(self, base_url: str, api_key: str = "") -> None:
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        if api_key:
            self.session.headers.update({"x-api-key": api_key})

    def _log_response(self, response: Response) -> None:
        print(f"[API] {response.request.method} {response.url} -> {response.status_code} ({response.elapsed.total_seconds():.2f}s)")

    def get(self, path: str, **kwargs) -> Response:
        url = f"{self.base_url}{path}"
        response = self.session.get(url, **kwargs)
        self._log_response(response)
        return response

    def post(self, path: str, **kwargs) -> Response:
        url = f"{self.base_url}{path}"
        response = self.session.post(url, **kwargs)
        self._log_response(response)
        return response

    def put(self, path: str, **kwargs) -> Response:
        url = f"{self.base_url}{path}"
        response = self.session.put(url, **kwargs)
        self._log_response(response)
        return response

    def patch(self, path: str, **kwargs) -> Response:
        url = f"{self.base_url}{path}"
        response = self.session.patch(url, **kwargs)
        self._log_response(response)
        return response

    def delete(self, path: str, **kwargs) -> Response:
        url = f"{self.base_url}{path}"
        response = self.session.delete(url, **kwargs)
        self._log_response(response)
        return response
