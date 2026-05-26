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

    def auth_client(self, login: str, password: str):
        response = self.dm_account_api.login_api.post_v1_account_login(json_data={
            'login': login,
            'password': password
        })
        token = {
            'x-dm-auth-token': response.headers['x-dm-auth-token']
        }
        self.dm_account_api.account_api.set_headers(token)
        self.dm_account_api.login_api.set_headers(token)

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

    def user_inactive_login(self, login: str, password: str):
        json_data_login = {
            'login': login,
            'password': password,
            'rememberMe': True,
        }
        response = self.dm_account_api.login_api.post_v1_account_login(json_data=json_data_login)
        assert response.status_code == 403, f'Oшибка 403 не была получена, получен статус код {response.status_code}'
        return response

    def get_current_user(self):
        response = self.dm_account_api.account_api.get_v1_account()
        assert response.status_code == 200, f'Данные текущего пользователя не были получены'
        return response

    def change_email(self, login: str, password: str, new_email: str):
        json_data_new_email = {
            'login': login,
            'password': password,
            'email': new_email
        }
        response = self.dm_account_api.account_api.put_v1_account_email(json_data=json_data_new_email)
        assert response.status_code == 200, f'Eмейл для пользователя {login} не был изменен'
        return response

    def change_password(self, login: str, password: str, email: str, new_password: str, auth_token: str):
        json_data = {
            'login': login,
            'email': email
        }
        response = self.dm_account_api.account_api.post_v1_account_password(json_data=json_data)
        assert response.status_code == 200, f'Пароль для пользователя {login} не был сброшен'
        token = self.get_activation_token_by_login(login, confirm='password')
        assert token is not None, f'Токен для пользователя {login} не был получен'
        json_data_new = {
            "login": login,
            "token": token,
            "oldPassword": password,
            "newPassword": new_password
        }
        response = self.dm_account_api.account_api.put_v1_account_password(auth_token=auth_token, json_data=json_data_new)
        assert response.status_code == 200, f'Пароль для пользователя {login} не был изменен'
        return response

    def user_activation(self, login: str):
        token = self.get_activation_token_by_login(login)
        assert token is not None, f'Токен для пользователя {login} не был получен'
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, f'Пользователь {login} не был активирован'
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
