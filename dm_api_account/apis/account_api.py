from restclient.client import RestClient


class AccountApi(RestClient):
    # Регистрация пользователя
    def post_v1_account(self, json_data):
        '''
        Register new user
        :param json_data:
        :return:
        '''
        response = self.post(path='/v1/account', json=json_data)
        return response

    # Получение пользователя
    def get_v1_account(self, **kwargs):
        '''
        Get current user
        :param kwargs:
        :return:
        '''
        response = self.get(path='/v1/account', **kwargs)
        return response

    # Активация пользователя
    def put_v1_account_token(self, token):
        '''
        Activate registered user
        :param token:
        :return:
        '''
        headers = {
            'accept': 'text/plain',
        }
        response = self.put(path=f'/v1/account/{token}', headers=headers)
        return response

    # Сброс пароля для зарегестрированного пользователя
    def post_v1_account_password(self, json_data):
        '''
        Reset registered user password
        :param json_data:
        :return:
        '''
        headers = {
            'accept': 'text/plain',
            'Content-Type': 'application/json'
        }
        response = self.post(path='/v1/account/password', headers=headers, json=json_data)
        return response

    def put_v1_account_password(self, json_data, **kwargs):
        '''
        Change registered user password
        :param json_data:
        :param kwargs:
        :return:
        '''
        response = self.put(path='/v1/account/password', json=json_data, **kwargs)
        return response

    # Изменение емейла
    def put_v1_account_email(self, json_data):
        '''
        Change registered user email
        :param json_data:
        :return:
        '''
        headers = {
            'accept': 'text/plain',
            'Content-Type': 'application/json'
        }
        response = self.put(path='/v1/account/email', headers=headers, json=json_data)
        return response
