import os
import httpx

from sentinel.models.token import Token
from sentinel.utils.logger import logger


SERVICE_ACCOUNT_TOKENS = {
    "HAAS_API_TOKEN": {
        "realm": "HAAS_REALM",
        "client_id": "HAAS_CLIENT_ID",
        "client_secret": "HAAS_CLIENT_SECRET",
    },
    "EXT_API_TOKEN": {
        "realm": "HACKEN_REALM",
        "client_id": "HACKEN_CLIENT_ID",
        "client_secret": "HACKEN_CLIENT_SECRET",
    },
}


class ServiceAccountToken:
    """
    Service Account Token
    """

    def __init__(self, endpoint_url: str, realm: str, client_id: str, client_secret) -> None:
        """
        Service Account Token Init
        """
        self._endpoint_url = endpoint_url
        self._realm = realm
        self._client_id = client_id
        self._client_secret = client_secret

        self.default_headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }

    def fetch(self) -> Token:
        """
        Fetch Service Account Token
        """
        headers = self.default_headers.copy()
        params = {
            "client_id": self._client_id,
            "client_secret": self._client_secret,
            "grant_type": "client_credentials",
        }
        endpoint = self._endpoint_url + f"/realms/{self._realm}/protocol/openid-connect/token"
        response = httpx.post(url=endpoint, data=params, headers=headers, verify=False)

        if response.status_code == 200:
            token_data = dict()
            for k, v in response.json().items():
                if k == "not-before-policy":
                    token_data["not_before_policy"] = v
                else:
                    token_data[k] = v
            return Token(**token_data)
        elif response.status_code == 404:
            return None
        else:
            raise RuntimeError(f"Request error, status code: {response.status_code}, response: {response.content}")


def import_service_tokens():
    """
    Import service tokens
    """
    endpoint = os.environ.get("AUTH_SERVICE_ENDPOINT_URL", None)
    if endpoint is None:
        raise AttributeError("Environment variable AUTH_SERVICE_ENDPOINT_URL missed")

    for token_name, vars in SERVICE_ACCOUNT_TOKENS.items():
        realm = os.environ.get(vars.get("realm")) if vars.get("realm") is not None else None
        client_id = os.environ.get(vars.get("client_id")) if vars.get("client_id") is not None else None
        client_secret = os.environ.get(vars.get("client_secret")) if vars.get("client_secret") is not None else None
        sa_token = ServiceAccountToken(
            endpoint_url=endpoint, realm=realm, client_id=client_id, client_secret=client_secret
        )
        token = sa_token.fetch()
        if token is not None:
            logger.info(f"Import service account token {token_name} as environment variable")
            os.environ[token_name] = token.access_token
        else:
            raise RuntimeError(f"Cannot import service account token from env: {token_name}")


if __name__ == "__main__":
    import argparse

    from sentinel.utils.settings import load_extra_vars

    parser = argparse.ArgumentParser()
    parser.add_argument("--env-vars", type=str, required=True, help="Set environment variables from JSON/YAML file")
    args = parser.parse_args()

    # Update env var from file
    for k, v in load_extra_vars([f"@{args.env_vars}"]).items():
        os.environ[k] = v

    import_service_tokens()
    for k, v in os.environ.items():
        if k.endswith("_TOKEN"):
            print(f"{k}: {v}")
