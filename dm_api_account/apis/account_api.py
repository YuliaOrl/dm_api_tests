import allure
from dm_api_account.models.change_email import ChangeEmail
from dm_api_account.models.change_password import ChangePassword
from dm_api_account.models.registration import Registration
from dm_api_account.models.reset_password import ResetPassword
from dm_api_account.models.user_details_envelope import UserDetailsEnvelope
from dm_api_account.models.user_envelope import UserEnvelope
from restclient.client import RestClient


class AccountApi(RestClient):

    @allure.step('Регистрация нового пользователя')
    def post_v1_account(self, registration: Registration):
        '''
        Register new user
        :param registration:
        :return:
        '''
        response = self.post(
            path='/v1/account',
            json=registration.model_dump(exclude_none=True, by_alias=True),
        )
        return response

    @allure.step('Получение информации о пользователе')
    def get_v1_account(self, validate_response=True, **kwargs):
        '''
        Get current user
        :param validate_response:
        :param kwargs:
        :return:
        '''
        response = self.get(
            path='/v1/account',
            **kwargs
        )
        if validate_response:
            return UserDetailsEnvelope(**response.json())
        return response

    @allure.step('Активация пользователя')
    def put_v1_account_token(self, token, validate_response=True):
        '''
        Activate registered user
        :param token:
        :param validate_response:
        :return:
        '''
        headers = {
            'accept': 'text/plain',
        }
        response = self.put(
            path=f'/v1/account/{token}',
            headers=headers,
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response

    @allure.step('Сброс пароля для зарегистрированного пользователя')
    def post_v1_account_password(self, reset_password: ResetPassword, validate_response=True):
        '''
        Reset registered user password
        :param reset_password:
        :param validate_response:
        :return:
        '''
        headers = {
            'accept': 'text/plain',
            'Content-Type': 'application/json'
        }
        response = self.post(
            path='/v1/account/password',
            headers=headers,
            json=reset_password.model_dump(exclude_none=True, by_alias=True),
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response

    @allure.step('Изменение пароля зарегистрированного пользователя')
    def put_v1_account_password(self, change_password: ChangePassword, validate_response=True, **kwargs):
        '''
        Change registered user password
        :param change_password:
        :param validate_response:
        :param kwargs:
        :return:
        '''
        response = self.put(
            path='/v1/account/password',
            json=change_password.model_dump(exclude_none=True, by_alias=True),
            **kwargs
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response

    @allure.step('Изменение емейла')
    def put_v1_account_email(self, change_email: ChangeEmail, validate_response=True):
        '''
        Change registered user email
        :param change_email:
        :param validate_response:
        :return:
        '''
        headers = {
            'accept': 'text/plain',
            'Content-Type': 'application/json'
        }
        response = self.put(
            path='/v1/account/email',
            headers=headers,
            json=change_email.model_dump(exclude_none=True, by_alias=True),
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response
