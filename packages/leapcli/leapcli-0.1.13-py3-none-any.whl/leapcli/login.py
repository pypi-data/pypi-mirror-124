import re
import logging
from toml import load, dump
from openapi_client import Configuration, ApiClient
from openapi_client.models import KeyLoginParams, UserData
from openapi_client.apis import DefaultApi
from leapcli.exceptions import MalformedKeys, KeysMixedUp, LoginFailed
from leapcli.project import Project

CREDENTIALS_FILENAME = 'credentials.toml'

_log = logging.getLogger(__name__)


class Authenticator:
    api_id: str = None
    api_key: str = None
    api_client: DefaultApi = None
    project: Project = None
    user: UserData = None
    cookie: str = None

    def __init__(self, project: Project):
        Authenticator.project = project
        _log.debug('initialized')

    @staticmethod
    def redact_key(key: str) -> str:
        assert len(key) > 3
        # Mask the first 19 characters of a key
        return '*' * 19 + key[-3:]

    @staticmethod
    def is_valid_api_key(api_key: str) -> bool:
        return re.match(r'^k0\w{20}$', api_key) is not None

    @staticmethod
    def is_valid_api_id(api_id: str) -> bool:
        return re.match(r'^i0\w{20}$', api_id) is not None

    @staticmethod
    def credentials_file_path() -> str:
        return Project.config_dir().joinpath(CREDENTIALS_FILENAME)

    @staticmethod
    def has_credentials() -> bool:
        api_id, api_key = Authenticator.read_credentials()
        return api_id is not None and api_key is not None

    @staticmethod
    def read_credentials() -> (str, str):
        # TODO: more robust handling of corrupted file
        path = Authenticator.credentials_file_path()
        if path.is_file():
            _log.debug('reading credentials from %s', path)
            with path.open('r') as f:
                dictionary = load(f)
                return dictionary['api_id'], dictionary['api_key']
        return None, None

    @staticmethod
    def write_credentials(api_id: str, api_key: str) -> None:
        _log.info('writing credentials')
        with Authenticator.credentials_file_path().open('w') as f:
            return dump(dict(api_id=api_id, api_key=api_key), f)

    @staticmethod
    def detect_api_id() -> str:
        api_id, _ = Authenticator.read_credentials()
        return api_id

    @staticmethod
    def detect_api_key() -> str:
        _, api_key = Authenticator.read_credentials()
        return api_key

    def prompt_api_id(self) -> str:
        default = self.detect_api_id()
        prompt = f'API ID [{Authenticator.redact_key(default)}]: ' if default else 'API ID: '
        return input(prompt) or default

    def prompt_api_key(self) -> str:
        default = self.detect_api_key()
        prompt = f'API Key [{Authenticator.redact_key(default)}]: ' if default else 'API Key: '
        return input(prompt) or default

    def key_login(self) -> None:
        host = Authenticator.project.detect_backend_url()
        cfg = Configuration(host=host)
        unauthenticated_client = ApiClient(cfg)
        api = DefaultApi(unauthenticated_client)
        params = KeyLoginParams(Authenticator.api_id, Authenticator.api_key)
        user, status, headers = api.key_login(params, _return_http_data_only=False)
        if status != 200 or not 'Set-Cookie' in headers:
            _log.info('login failed with api_id: %s, api_key: %s', Authenticator.api_id,
                      self.redact_key(Authenticator.api_key))
            raise LoginFailed()
        Authenticator.user = user
        Authenticator.cookie = headers['Set-Cookie']

    @staticmethod
    def load_credentials() -> None:
        Authenticator.api_id = Authenticator.detect_api_id()
        Authenticator.api_key = Authenticator.detect_api_key()

    @staticmethod
    def logged_in() -> bool:
        return Authenticator.cookie is not None

    def authenticated_api(self) -> DefaultApi:
        if not self.logged_in():
            self.key_login()
        host = Authenticator.project.detect_backend_url()
        cfg = Configuration(host=host)
        cookie_client = ApiClient(cfg, cookie=self.cookie)

        return DefaultApi(cookie_client)

    def cli_login(self, api_id: str = None, api_key: str = None):
        api_id = api_id or self.prompt_api_id()
        if not Authenticator.is_valid_api_id(api_id):
            if Authenticator.is_valid_api_key(api_id):
                raise KeysMixedUp()
            raise MalformedKeys()
        Authenticator.api_id = api_id
        api_key = api_key or self.prompt_api_key()
        if not Authenticator.is_valid_api_key(api_key):
            raise MalformedKeys()
        Authenticator.api_key = api_key
        self.authenticated_api()
        print(f'Authenticated as {Authenticator.user.local.email}')
        self.write_credentials(Authenticator.api_id, Authenticator.api_key)
