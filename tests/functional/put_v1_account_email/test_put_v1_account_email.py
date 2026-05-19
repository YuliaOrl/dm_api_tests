from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi
from random import randint


def test_put_v1_account_email():
    # Регистрация пользователя
    account_api = AccountApi(host='http://185.185.143.231:5051')
    login_api = LoginApi(host='http://185.185.143.231:5051')
    mailhog_api = MailhogApi(host='http://185.185.143.231:5025')

    login = 'Lola_' + str(randint(10000, 99999))  # Zolushka
    password = '135792468'
    email = f'{login}@yandex.ru'

    json_data = {
        'login': login,
        'email': email,
        'password': password
    }

    response = account_api.post_v1_account(json_data=json_data)
    print(response.status_code, response.text, sep='\n')
    assert response.status_code == 201, f'Пользователь не был создан {response.json()}'

    # Получение писем из почтового сервера
    response = mailhog_api.get_api_v2_messages()
    print(response.status_code, response.text, sep='\n')
    assert response.status_code == 200, 'Письма не были получены'

    # Получение активационного токена
    token = mailhog_api.get_activation_token_by_login(login, response)
    assert token is not None, f'Токен для пользователя {login} не был получен'

    # Активация пользователя
    response = account_api.put_v1_account_token(token=token)
    print(response.status_code, response.text, sep='\n')
    assert response.status_code == 200, f'Пользователь {login} не был активирован'

    # Авторизация пользователя
    json_data_login = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = login_api.post_v1_account_login(json_data=json_data_login)
    print(response.status_code, response.text, sep='\n')
    assert response.status_code == 200, f'Пользователь {login} не был авторизован'

    # Изменение емейла
    json_data_new_email = {
        'login': login,
        'password': password,
        'email': email.replace('@', '_new_email@')
    }
    response = account_api.put_v1_account_email(json_data=json_data_new_email)
    print(response.status_code, response.text, sep='\n')
    assert response.status_code == 200, f'Eмейл для пользователя {login} не был изменен'

    # Авторизация пользователя после смены емейла и получение ошибки 403
    response = login_api.post_v1_account_login(json_data=json_data_login)
    print(response.status_code, response.text, sep='\n')
    assert response.status_code == 403, f'Oшибка 403 не была получена, получен статус код {response.status_code}'

    # Получение писем из почтового сервера и получение нового активационного токена для подтверждения смены емейла
    response = mailhog_api.get_api_v2_messages()
    print(response.status_code, response.text, sep='\n')
    assert response.status_code == 200, 'Письма после смены емейла не были получены'

    token = mailhog_api.get_activation_token_by_login(login, response)
    assert token is not None, f'Токен после смены емейла для пользователя {login} не был получен'

    # Активация токена
    response = account_api.put_v1_account_token(token=token)
    print(response.status_code, response.text, sep='\n')
    assert response.status_code == 200, f'Пользователь {login} не был активирован'

    # Авторизация пользователя после смены емейла и активации нового токена
    response = login_api.post_v1_account_login(json_data=json_data_login)
    print(response.status_code, response.text, sep='\n')
    assert response.status_code == 200, f'Пользователь {login} не был авторизован'
