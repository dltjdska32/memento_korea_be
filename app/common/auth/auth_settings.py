from pydantic_settings import BaseSettings


class AuthSettings(BaseSettings):

    # api 화이트리스트
    api_whitelist: list[str] = [
        "/api/auth/login",
        "/api/auth/logout",
        "/api/auth/join",
        "/api/auth/reissue",

        "/docs",
        "/openapi.json",
        "/redoc",

    ]

    def is_whitelisted(self, path: str) -> bool:
        for pattern in self.api_whitelist:

            if pattern.endswith("/**"):

                prefix = pattern[:-3]

                if path == prefix or path.startswith(f"{prefix}/"):
                    return True
                continue

            if path == pattern:
                return True

        return False


auth_settings: AuthSettings = AuthSettings()