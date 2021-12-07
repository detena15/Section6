from code.models import UserModel


def authenticate(username, password):
    user = UserModel.find_by_username(username)  # Find the user in the database
    if user and user.password == password:
        return user


def identity(payload):  # The payload is the contects of the JWT (json web token)
    user_id = payload['identity']  # Extract the user_id from that payload
    return UserModel.find_by_id(user_id)
