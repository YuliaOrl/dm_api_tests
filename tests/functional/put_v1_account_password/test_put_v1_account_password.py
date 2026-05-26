def test_put_v1_account_password(account_helper, prepare_user):
    # Проверка изменения пароля пользователя
    login, password, email = prepare_user.login, prepare_user.password, prepare_user.email
    new_password = password[::-1]

    account_helper.register_new_user(login=login, password=password, email=email)
    account_helper.auth_client(login=login, password=password)
    account_helper.change_password(login=login, password=password, email=email, new_password=new_password)
    account_helper.user_login(login=login, password=new_password)


