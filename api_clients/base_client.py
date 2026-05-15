import json

import allure
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

    def _attach_response(self, response: Response) -> None:
        allure.attach(
            json.dumps({
                "url": response.url,
                "status": response.status_code,
                "headers": dict(response.headers),
                "body": response.text[:2000],
            }, indent=2, ensure_ascii=False),
            name=f"{response.request.method} {response.url}",
            attachment_type=allure.attachment_type.JSON,
        )

    def get(self, path: str, **kwargs) -> Response:
        url = f"{self.base_url}{path}"
        with allure.step(f"GET {path}"):
            response = self.session.get(url, **kwargs)
            self._attach_response(response)
        return response

    def post(self, path: str, **kwargs) -> Response:
        url = f"{self.base_url}{path}"
        with allure.step(f"POST {path}"):
            response = self.session.post(url, **kwargs)
            self._attach_response(response)
        return response

    def put(self, path: str, **kwargs) -> Response:
        url = f"{self.base_url}{path}"
        with allure.step(f"PUT {path}"):
            response = self.session.put(url, **kwargs)
            self._attach_response(response)
        return response

    def patch(self, path: str, **kwargs) -> Response:
        url = f"{self.base_url}{path}"
        with allure.step(f"PATCH {path}"):
            response = self.session.patch(url, **kwargs)
            self._attach_response(response)
        return response

    def delete(self, path: str, **kwargs) -> Response:
        url = f"{self.base_url}{path}"
        with allure.step(f"DELETE {path}"):
            response = self.session.delete(url, **kwargs)
            self._attach_response(response)
        return response
