""" Utilities for the Python SDK of the YooniK BiometricInThings API.
"""
import base64
import os
import typing
import requests


class YoonikBitException(Exception):
    """Custom Exception for the python SDK of the YooniK BiometricInThings API."""
    def __init__(self, status_code, message):
        """ Class initializer.
        :param status_code: HTTP responde status code.
        :param message: Error message.
        """
        super(YoonikBitException, self).__init__()
        self.status_code = status_code
        self.message = message

    def __str__(self):
        return ('Error when calling YooniK BiometricInThings API:\n'
                '\tstatus_code: {}\n'
                '\tmessage: {}\n').format(self.status_code, self.message)


class Key:
    """Manage YooniK BiometricInThings API Subscription Key."""

    @classmethod
    def set(cls, key: str):
        """Set the Subscription Key.
        :param key:
        :return:
        """
        cls.key = key

    @classmethod
    def get(cls) -> typing.Union[str, None]:
        """Get the Subscription Key.
        :return:
        """
        if not hasattr(cls, 'key'):
            cls.key = None
        return cls.key


class BaseUrl:
    """Manage YooniK BiometricInThings API Base URL."""

    @classmethod
    def set(cls, base_url: str):
        if not base_url.endswith('/'):
            base_url += '/'
        cls.base_url = base_url

    @classmethod
    def get(cls) -> typing.Union[str, None]:
        if not hasattr(cls, 'base_url'):
            cls.base_url = None
        return cls.base_url


def request(method, url, data=None, json=None, headers=None, params=None):
    # pylint: disable=too-many-arguments
    """ Universal interface for request."""
    url = BaseUrl.get() + url

    # Setup the headers with default Content-Type and Subscription Key.
    headers = headers or {}
    if 'Content-Type' not in headers and method != 'GET':
        headers['Content-Type'] = 'application/json'
    api_key = Key.get()
    if api_key:
        headers['x-api-key'] = api_key

    response = requests.request(
        method,
        url,
        params=params,
        data=data,
        json=json,
        headers=headers)

    if not response.ok:
        raise YoonikBitException(response.status_code, response.text)

    return response.json() if response.text and method != 'GET' else {}


def parse_image(image) -> str:
    """Check whether the image is a string or a file path or a file-like object.
    :param image:
        A base64 string or a file path or a file-like object representing an image.
    :return:
        Image as a base64 string.
    """
    data = None
    try:
        if hasattr(image, 'read'):  # When image is a file-like object.
            data = image.read()
        elif os.path.isfile(image):  # When image is a file path.
            data = open(image, 'rb').read()
    except ValueError as value_error:
        if not value_error.__str__().__contains__("path too long"):
            raise value_error
    return base64.b64encode(data).decode('utf-8') if data else image
