from restclient.client import RestClient


class LoginApi(RestClient):
    # Авторизация пользователя
    def post_v1_account_login(self, json_data):
        '''
        Authenticate via credentials
        :param json_data:
        :return:
        '''
        response = self.post(path='/v1/account/login', json=json_data)
        return response
