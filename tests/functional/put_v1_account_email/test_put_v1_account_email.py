def test_put_v1_account_email(account_helper, prepare_user):
    # Проверка изменения емейла пользователя
    login, password, email = prepare_user.login, prepare_user.password, prepare_user.email
    new_email = email.replace('@', '_new_email@')

    account_helper.register_new_user(login=login, password=password, email=email)
    account_helper.user_login(login=login, password=password)
    account_helper.change_email(login=login, password=password, new_email=new_email)
    account_helper.user_login(login=login, password=password, expected_status=403)
    account_helper.user_activation(login=login)
    account_helper.user_login(login=login, password=password)
