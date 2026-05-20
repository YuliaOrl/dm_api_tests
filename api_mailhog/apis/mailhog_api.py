from json import loads

from restclient.client import RestClient


class MailhogApi(RestClient):
    # Получить письма из почтового сервера
    def get_api_v2_messages(self, limit=50):
        '''
        Get Users emails
        :return:
        '''
        params = {
            'limit': limit,
        }
        response = self.get(path='/api/v2/messages', params=params, verify=False)
        return response

    # Получить активационный токен
    def get_activation_token_by_login(self, login, response):
        for item in response.json().get('items', []):
            user_data = loads(item.get('Content', {}).get('Body'))
            if user_data.get('Login') == login:
                token = user_data.get('ConfirmationLinkUrl', '').split('/')[-1]
                if token:
                    print(f'Login: {login}, token: {token}')
                    return token
        return None
