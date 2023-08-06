import json
import requests

from typing import Dict

from .decorator import http_exception


class Request:
    def __init__(self, validation: bool) -> None:
        self._requester_base = requests
        self.validation = validation

    @http_exception
    def get(self, url: str, headers: Dict = {}, query_params: Dict = {}):
        print('here, get')
        if self.validation is False:
            print('get, false')
            return self._requester_base.get(url, headers=headers, params=query_params, verify=False)
        else:
            return self._requester_base.get(url, headers=headers, params=query_params)

    @http_exception
    def post(self, url: str, headers: Dict = {}, data: Dict = {}):
        print('here, post')
        if self.validation is False:
            print('post, false')
            return self._requester_base.post(url, headers=headers, data=json.dumps(data), verify=False)
        else:
            return self._requester_base.post(url, headers=headers, data=json.dumps(data))

    @http_exception
    def put(self, url: str, headers: Dict = {}, data: Dict = {}):
        print('here, put')
        if self.validation is False:
            return self._requester_base.put(url, headers=headers, data=json.dumps(data), verify=False)
        else:
            return self._requester_base.put(url, headers=headers, data=json.dumps(data))

    @http_exception
    def delete(self, url: str, headers: Dict = {}):
        if self.validation is False:
            return self._requester_base.delete(url, headers=headers, verify=False)
        else:
            return self._requester_base.delete(url, headers=headers)
