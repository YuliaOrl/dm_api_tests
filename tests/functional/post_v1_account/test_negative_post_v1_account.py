import pytest
from collections import namedtuple
from datetime import datetime
from checkers.http_checkers import check_status_code_http
from dm_api_account.models.registration import Registration


def new_user():
    now = datetime.now()
    time = now.strftime('%H_%M_%S_%f')
    login = f'Testov_{time}'
    password = '123456789'
    email = f'{login}@yandex.ru'
    User = namedtuple('User', ['login', 'password', 'email'])
    user = User(login=login, password=password, email=email)
    return user

user = new_user()

@pytest.mark.parametrize('error_message, registration', [
        [{"Password": ["Short"]}, Registration(login=user.login, email=user.email, password=user.password[:5])],
        [{"Email": ["Invalid"]}, Registration(login=user.login, email=user.email.replace('@', ''), password=user.password)],
        [{"Login": ["Short"]}, Registration(login=user.login[0], email=user.email, password=user.password)],
])
def test_negative_post_v1_account(account_helper, error_message, registration):
    # Негативная проверка регистрации пользователя
    with check_status_code_http(
            expected_status_code=400,
            expected_title_message='Validation failed',
            expected_error_message=error_message
        ):
        account_helper.dm_account_api.account_api.post_v1_account(registration=registration)
