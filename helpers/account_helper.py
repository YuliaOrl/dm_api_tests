import time
from json import loads
from dm_api_account.models.change_email import ChangeEmail
from dm_api_account.models.change_password import ChangePassword
from dm_api_account.models.login_credentials import LoginCredentials
from dm_api_account.models.registration import Registration
from dm_api_account.models.reset_password import ResetPassword
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi


def retrier(function):
    def wrapper(*args, **kwargs):
        token = None
        cnt = 1
        while token is None:
            print(f'Попытка получения токена номер {cnt}!')
            token = function(*args, **kwargs)
            cnt += 1
            if cnt == 6:
                raise AssertionError('Превышено количество попыток получения токена активации!')
            if token:
                return token
            time.sleep(1)

    return wrapper


class AccountHelper:
    def __init__(self, dm_account_api: DMApiAccount, mailhog: MailHogApi):
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog

    def auth_client(self, login: str, password: str, validate_response=False):
        login_credentials = LoginCredentials(
            login=login,
            password=password,
            remember_me=True
        )
        response = self.dm_account_api.login_api.post_v1_account_login(
            login_credentials=login_credentials,
            validate_response=validate_response
        )
        token = {
            'x-dm-auth-token': response.headers['x-dm-auth-token']
        }
        self.dm_account_api.account_api.set_headers(token)
        self.dm_account_api.login_api.set_headers(token)

    def register_new_user(self, login: str, password: str, email: str):
        registration = Registration(
            login=login,
            email=email,
            password=password
        )
        response = self.dm_account_api.account_api.post_v1_account(registration=registration)
        assert response.status_code == 201, f'Пользователь не был создан {response.json()}'
        response = self.user_activation(login=login)
        return response

    def user_login(self, login: str, password: str, remember_me: bool = True, expected_status: int = 200, validate_response=False):
        login_credentials = LoginCredentials(
            login=login,
            password=password,
            remember_me=remember_me
        )
        response = self.dm_account_api.login_api.post_v1_account_login(
            login_credentials=login_credentials,
            validate_response=validate_response
        )
        if expected_status == 200:
            assert response.headers['x-dm-auth-token'], f'Токен для пользователя {login} не был получен'
        assert response.status_code == expected_status, f'Ожидается статус код {expected_status}, получен {response.status_code}'
        return response

    def get_current_user(self):
        response = self.dm_account_api.account_api.get_v1_account()
        return response

    def change_email(self, login: str, password: str, new_email: str):
        change_email = ChangeEmail(
            login=login,
            password=password,
            email=new_email
        )
        response = self.dm_account_api.account_api.put_v1_account_email(change_email=change_email)
        return response

    def change_password(self, login: str, password: str, email: str, new_password: str):
        reset_password = ResetPassword(
            login=login,
            email=email
        )
        self.dm_account_api.account_api.post_v1_account_password(reset_password=reset_password)
        token = self.get_activation_token_by_login(login, confirm='password')
        assert token is not None, f'Токен для пользователя {login} не был получен'
        change_password = ChangePassword(
            login=login,
            token=token,
            old_password=password,
            new_password=new_password
        )
        response = self.dm_account_api.account_api.put_v1_account_password(change_password=change_password)
        return response

    def user_activation(self, login: str):
        token = self.get_activation_token_by_login(login)
        assert token is not None, f'Токен для пользователя {login} не был получен'
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        return response

    def user_logout(self):
        response = self.dm_account_api.login_api.delete_v1_account_login()
        assert response.status_code == 204, f'Выход из аккаунта не был выполнен'
        return response

    def user_logout_all(self):
        response = self.dm_account_api.login_api.delete_v1_account_login_all()
        assert response.status_code == 204, f'Выход из аккаунта на всех устройствах не был выполнен'
        return response

    # Получение активационного токена
    @retrier
    def get_activation_token_by_login(self, login, confirm='activate'):
        conf_token = {
            'activate': 'ConfirmationLinkUrl',
            'password': 'ConfirmationLinkUri'
        }
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        for item in response.json().get('items', []):
            user_data = loads(item.get('Content', {}).get('Body'))
            if user_data.get('Login') == login:
                token = user_data.get(conf_token[confirm], '').split('/')[-1]
                if token:
                    print(f'Login: {login}, token: {token}')
                    return token
        return None
