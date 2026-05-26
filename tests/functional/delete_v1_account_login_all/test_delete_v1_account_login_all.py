def test_delete_v1_account_login_all(auth_account_helper):
    # Проверка выхода авторизованного пользователя из аккаунта на всех устройствах
    auth_account_helper.user_logout_all()