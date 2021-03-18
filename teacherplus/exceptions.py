RESET_PASSWORD_TOKEN_INVALID = "The token for the reset password is not valid"


class DataNullOrTokenInvalidException(Exception):
    """
    This class is inherited from the exception to specify the invalidity
    of the reset password token that is beng used to verify
    """

    def __init__(self):
        super(DataNullOrTokenInvalidException, self).__init__(
            RESET_PASSWORD_TOKEN_INVALID
        )
