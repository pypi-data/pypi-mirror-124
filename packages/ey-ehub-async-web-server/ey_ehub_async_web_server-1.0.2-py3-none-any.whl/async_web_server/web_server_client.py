import time
import logging
import requests
from http import HTTPStatus


class EHubWebServerClient(object):

    DEFAULT_WEB_SERVER_URL = 'http://127.0.0.1'
    DEFAULT_WEB_SERVER_PORT = 5000

    _REQUEST_FINAL_STATES = [HTTPStatus.OK,
                             HTTPStatus.NOT_FOUND,
                             HTTPStatus.INTERNAL_SERVER_ERROR]


class EHubWebServerAsynchronousClient(EHubWebServerClient):

    _SUBMIT_REQUEST_ENDPOINT = 'submit-request'
    _GET_REQUEST_STATE_ENDPOINT = 'get-request-state'

    def __init__(self,
                 server_url=EHubWebServerClient.DEFAULT_WEB_SERVER_URL,
                 server_port=EHubWebServerClient.DEFAULT_WEB_SERVER_PORT):
        self._endpoint = f'{server_url}:{server_port}'

    def submit_request(self, function_name, **function_call_args):
        logging.debug(f'Submit request: "{function_name}", call args: {function_call_args}')
        return requests.post(f'{self._endpoint}/{self._SUBMIT_REQUEST_ENDPOINT}',
                             json={'function': function_name, 'call_args': function_call_args})

    def get_request_state(self, request_id):
        logging.debug(f'Get request state for request ID: {request_id}')
        return requests.get(f'{self._endpoint}/{self._GET_REQUEST_STATE_ENDPOINT}/{request_id}')


class EHubWebServerSynchronousClient(EHubWebServerClient):

    POLLING_STATE_FREQUENCY = 2 # in seconds

    def __init__(self,
                 server_url=EHubWebServerClient.DEFAULT_WEB_SERVER_URL,
                 server_port=EHubWebServerClient.DEFAULT_WEB_SERVER_PORT,
                 request_polling_freq=POLLING_STATE_FREQUENCY):
        self._async_client = EHubWebServerAsynchronousClient(server_url,
                                                             server_port)
        self._request_polling_freq = request_polling_freq

    def call(self, function_name, **kwargs):
        logging.info(f'Call server function name: "{function_name}", call args: {kwargs}')
        response = self._async_client.submit_request(function_name, **kwargs)
        if response.status_code == HTTPStatus.CREATED:
            return self._poll_request_until_handled(response.text)
        logging.info(f'Return response with status code: {response.status_code}'
                     f' and text: "{response.text}"')
        return response

    def _poll_request_until_handled(self, request_id):
        while True:
           response = self._async_client.get_request_state(request_id)
           if response.status_code in self._REQUEST_FINAL_STATES:
               return response
           time.sleep(self._request_polling_freq)
