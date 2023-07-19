from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp) -> str:
        return {
            super()._make_hash_value(user, timestamp)
        }

generate_token = TokenGenerator()