def test_delete_v1_account_login(new_auth_account_helper):
    # Проверка выхода авторизованного пользователя из аккаунта
    new_auth_account_helper.user_logout()
