"""
Owner: Noctsol
Contributors: N/A
Date Created: 2021-10-24

Summary:
    Holds all the custom Exceptions for this project
"""


############################ EXCEPTIONS ############################

class EnvVarNotSet(Exception):
    '''Exception for when we didn't load'''

    def __init__(self):
        self.message = "Environment not set - please call Environment.load_env()"
        super().__init__(self.message)

class EnvVarNotExistError(Exception):
    '''Exception for when we call a nonexistent item'''

    def __init__(self, env_key):
        self.message = f"Environment variable key '{env_key}' not found"
        super().__init__(self.message)

class EnvVarEmptyError(Exception):
    '''Exception for when a environment var is empty or null'''

    def __init__(self, env_key):
        self.message = f"Environment variable key '{env_key}' has an empty or null value"
        super().__init__(self.message)

class EnvFileNotExist(Exception):
    '''Exception for when .env file is not found'''

    def __init__(self, path_list):
        paths_string = ", ".join(path_list)
        self.message = f"Create an env file please. Unable to find .env file in any of the following paths: {paths_string}"
        super().__init__(self.message)
