from checkers.get_v1_account import GetV1Account
from checkers.http_checkers import check_status_code_http


def test_get_v1_account_auth(auth_account_helper, prepare_user):
    # Позитивная проверка получения информации о пользователе
    with check_status_code_http():
        response = auth_account_helper.get_current_user()
        GetV1Account.check_response_values(response, prepare_user)


def test_get_v1_account_no_auth(account_helper):
    # Негативная проверка получения информации о неавторизованном пользователе
    with check_status_code_http(401, 'User must be authenticated'):
        account_helper.get_current_user()
