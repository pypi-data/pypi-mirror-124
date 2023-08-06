

class VEnvError(Exception):
    """Generic exception for VEnv"""


class VEnvOutputError(VEnvError):
    """Invalid output from command"""