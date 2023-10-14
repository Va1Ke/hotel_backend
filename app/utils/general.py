import os
import enum


def get_env_value(env_variable):
    try:
        return os.environ[env_variable]
    except KeyError:
        raise 'Set the' + str(env_variable) + 'environment variable'


class ServiceKind(enum.Enum):
    Standart = "Standart"
    Business = "Business"
    President = "President"
