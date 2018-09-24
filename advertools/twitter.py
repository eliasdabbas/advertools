from functools import wraps

from twython import Twython
import pandas as pd


def authenticate(func):
    auth_params = {}
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    def set_auth_params(**params):
        nonlocal auth_params
        auth_params.update(params)

    def get_auth_params():
        return auth_params

    wrapper.set_auth_params = set_auth_params
    wrapper.get_auth_params = get_auth_params
    return wrapper