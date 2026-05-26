def test_post_v1_account(account_helper, prepare_user):
    # Проверка регистрации пользователя
    login, password, email = prepare_user.login, prepare_user.password, prepare_user.email

    account_helper.register_new_user(login=login, password=password, email=email)
    account_helper.user_login(login=login, password=password)
