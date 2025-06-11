from urllib.parse import urlencode

import aiohttp

class YandexOauthAPI:
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret

        self.auth_url = "https://oauth.yandex.ru/authorize"
        self.token_url = "https://oauth.yandex.ru/token"
        self.info_url = "https://login.yandex.ru/info"

    def build_auth_url(
            self,
            device_id: str = None,
            device_name: str = None,
            login_hint: str = None,
            scope: str = None,
            optional_scope: str = None,
            force_confirm: bool = False,
            state: str = None,
            code_challenge: str = None,
            code_challenge_method: str = "plain") -> str:
        params = {
            "response_type": "code",
            "client_id": self.client_id
        }

        if device_id:
            params["device_id"] = device_id
        if device_name:
            params["device_name"] = device_name
        if login_hint:
            params["login_hint"] = login_hint
        if scope:
            params["scope"] = scope
        if optional_scope:
            params["optional_scope"] = optional_scope
        if force_confirm:
            params["force_confirm"] = "yes"
        if state:
            params["state"] = state
        if code_challenge:
            params["code_challenge"] = code_challenge
            params["code_challenge_method"] = code_challenge_method

        return f"{self.auth_url}?{urlencode(params)}"


    async def get_token(self, code: str) -> dict:
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self. token_url, data=data) as response:
                return await response.json()

    async def get_info_by_token(
            self,
            access_token: str,
            format: str = "json",
            jwt_secret: str = None) -> dict:

        if format not in ("json", "xml", "jwt"):
            raise ValueError("Недопустимый формат. Допустимые значения: json, xml, jwt")

        params = {"format": format}
        if format == "jwt" and jwt_secret:
            params["jwt_secret"] = jwt_secret

        headers = {"Authorization": f"OAuth {access_token}"}
        async with aiohttp.ClientSession() as session:
            async with session.get(self.info_url, params=params, headers=headers) as response:
                return await response.json()

