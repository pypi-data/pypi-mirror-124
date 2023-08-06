import os
from logging import Logger, LoggerAdapter
from typing import Optional, Union

from .default_logger import DefaultLogger
from .exceptions import ConfigError
from .socrates.url_validator import is_valid_url


class Config(object):
    KEYCLOAK_SERVER_URL = "https://auth.paretos.io/auth/"
    KEYCLOAK_REALM_NAME = "paretos"
    KEYCLOAK_CLIENT_ID = "main"

    def __init__(
        self,
        username: str = "",
        password: str = "",
        keycloak_server_url: str = KEYCLOAK_SERVER_URL,
        keycloak_realm_name: str = KEYCLOAK_REALM_NAME,
        keycloak_socrates_api_client_id: str = KEYCLOAK_CLIENT_ID,
        socrates_url: str = None,
        logger: Optional[Union[Logger, LoggerAdapter]] = None,
        dashboard_host: str = "127.0.0.1",
        dashboard_port: str = "8080",
    ):
        self.__username = username
        self.__password = password
        self.__keycloak_server_url = keycloak_server_url
        self.__keycloak_realm_name = keycloak_realm_name
        self.__keycloak_socrates_api_client_id = keycloak_socrates_api_client_id
        self.__dashboard_host = dashboard_host
        self.__dashboard_port = dashboard_port

        self.__set_socrates_url(
            socrates_url
            or os.environ.get('SOCRATES_URL')
            or "https://api.paretos.io/socrates/")
        self.__logger = logger or DefaultLogger()

    def get_username(self) -> str:
        return self.__username

    def get_password(self) -> str:
        return self.__password

    def get_keycloak_server_url(self) -> str:
        return self.__keycloak_server_url

    def get_keycloak_realm_name(self) -> str:
        return self.__keycloak_realm_name

    def get_keycloak_socrates_api_client_id(self) -> str:
        return self.__keycloak_socrates_api_client_id

    def __set_socrates_url(self, api_url: str):
        if not is_valid_url(api_url):
            raise ConfigError(f"'{api_url}' is not a valid url")

        if api_url[len(api_url) - 1] != "/":
            api_url = api_url + "/"

        self.__socrates_url = api_url

    def get_api_url(self) -> str:
        return self.__socrates_url

    def get_logger(self) -> Logger:
        return self.__logger

    def get_dashboard_host(self) -> str:
        return self.__dashboard_host

    def get_dashboard_port(self) -> str:
        return self.__dashboard_port
