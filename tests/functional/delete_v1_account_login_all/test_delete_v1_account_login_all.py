def test_delete_v1_account_login_all(new_auth_account_helper):
    # Проверка выхода авторизованного пользователя из аккаунта на всех устройствах
    new_auth_account_helper.user_logout_all()