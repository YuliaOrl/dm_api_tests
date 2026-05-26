from helpers.account_helper import AccountHelper
from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DMApiConfiguration
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi
from random import randint
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


def test_put_v1_account_email():
    # Проверка изменения емейла пользователя
    dm_api_configuration=DMApiConfiguration(host='http://185.185.143.231:5051', disable_log=False)
    mailhog_configuration = MailhogConfiguration(host='http://185.185.143.231:5025')

    account = DMApiAccount(configuration=dm_api_configuration)
    mailhog = MailHogApi(configuration=mailhog_configuration)
    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)

    login = 'Zolushka_' + str(randint(10000, 99999))
    password = '135792468'
    email = f'{login}@yandex.ru'
    new_email = email.replace('@', '_new_email@')

    account_helper.register_new_user(login=login, password=password, email=email)
    account_helper.user_login(login=login, password=password)
    account_helper.change_email(login=login, password=password, new_email=new_email)
    account_helper.user_inactive_login(login=login, password=password)
    account_helper.user_activation(login=login)
    account_helper.user_login(login=login, password=password)
