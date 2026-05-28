import pytest
from datetime import datetime
from collections import namedtuple
from helpers.account_helper import AccountHelper
from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DMApiConfiguration
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi
import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=True,
            # sort_keys=True
        )
    ]
)


@pytest.fixture(scope='session')
def account_api():
    dm_api_configuration = DMApiConfiguration(host='http://185.185.143.231:5051', disable_log=False)
    account = DMApiAccount(configuration=dm_api_configuration)
    return account


@pytest.fixture(scope='session')
def mailhog_api():
    mailhog_configuration = MailhogConfiguration(host='http://185.185.143.231:5025')
    mailhog_client = MailHogApi(configuration=mailhog_configuration)
    return mailhog_client


@pytest.fixture()
def account_helper(account_api, mailhog_api):
    account_helper = AccountHelper(dm_account_api=account_api, mailhog=mailhog_api)
    return account_helper


@pytest.fixture()
def auth_account_helper(account_api, mailhog_api, prepare_user):
    auth_account_helper = AccountHelper(dm_account_api=account_api, mailhog=mailhog_api)
    auth_account_helper.register_new_user(login=prepare_user.login, password=prepare_user.password, email=prepare_user.email)
    auth_account_helper.auth_client(login=prepare_user.login, password=prepare_user.password)
    return auth_account_helper


@pytest.fixture
def prepare_user():
    now = datetime.now()
    time = now.strftime('%H_%M_%S_%f')
    login = f'Zolushka_{time}'
    password = '987654321'
    email = f'{login}@yandex.ru'
    User = namedtuple('User', ['login', 'password', 'email'])
    user = User(login=login, password=password, email=email)
    return user
