from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)


"""
Here i'm creating class Hasher that will be used to hash passwords and verify passwords.
I used @staticmethod because the methods dont depend on the state of the class instance
"""