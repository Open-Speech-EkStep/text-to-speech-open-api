import os

def get_env_var(var_name=str, default=''):
    return os.environ.get(var_name, default)

