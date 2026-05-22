import time
from json import loads
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

    def register_new_user(self, login: str, password: str, email: str):
        json_data = {
            'login': login,
            'email': email,
            'password': password
        }
        response = self.dm_account_api.account_api.post_v1_account(json_data=json_data)
        assert response.status_code == 201, f'Пользователь не был создан {response.json()}'
        response = self.user_activation(login=login)
        return response

    def user_login(self, login: str, password: str, remember_me: bool = True):
        json_data_login = {
            'login': login,
            'password': password,
            'rememberMe': remember_me,
        }
        response = self.dm_account_api.login_api.post_v1_account_login(json_data=json_data_login)
        assert response.status_code == 200, f'Пользователь не был авторизован'
        return response

    def change_email(self, login: str, password: str, email: str):
        json_data_new_email = {
            'login': login,
            'password': password,
            'email': email.replace('@', '_new_email@')
        }
        response = self.dm_account_api.account_api.put_v1_account_email(json_data=json_data_new_email)
        assert response.status_code == 200, f'Eмейл для пользователя {login} не был изменен'
        json_data_login = {
            'login': login,
            'password': password,
            'rememberMe': True,
        }
        response = self.dm_account_api.login_api.post_v1_account_login(json_data=json_data_login)
        assert response.status_code == 403, f'Oшибка 403 не была получена, получен статус код {response.status_code}'
        response = self.user_activation(login=login)
        return response

    def user_activation(self, login: str):
        token = self.get_activation_token_by_login(login)
        assert token is not None, f'Токен для пользователя {login} не был получен'
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, f'Пользователь {login} не был активирован'
        return response

    # Получение активационного токена
    @retrier
    def get_activation_token_by_login(self, login):
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        for item in response.json().get('items', []):
            user_data = loads(item.get('Content', {}).get('Body'))
            if user_data.get('Login') == login:
                token = user_data.get('ConfirmationLinkUrl', '').split('/')[-1]
                if token:
                    print(f'Login: {login}, token: {token}')
                    return token
        return None

