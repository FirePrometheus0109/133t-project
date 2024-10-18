from django.contrib.auth.tokens import PasswordResetTokenGenerator

from django.utils.crypto import constant_time_compare
from django.utils.http import base36_to_int


class RestoreAccountTokenGenerator(PasswordResetTokenGenerator):

    def check_token(self, user, token):
        """
        Checks user token the same way as parent checks excepting reset timeout
        """
        if not (user and token):
            return False
        # Parse the token
        try:
            ts_b36, hash = token.split("-")  # noqa
        except ValueError:
            return False

        try:
            ts = base36_to_int(ts_b36)
        except ValueError:
            return False

        # Check that the timestamp/uid has not been tampered with
        if not constant_time_compare(
                self._make_token_with_timestamp(user, ts),
                token):
            return False

        return True
