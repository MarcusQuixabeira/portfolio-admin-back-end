from datetime import datetime
from src.v1.models import User
from src.config.db import PSQLConfig
from passlib.context import CryptContext

class CreateAdminUserScript(object):
    """
    It creates the admin user that holds the credentials to manipulate
    the data using the Admin API.
    
    Call execute() to create the user in the context DB.
    """
    def __init__(self):
        self.bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
        self.db_session = PSQLConfig().get_local_session()

    def __receive_data(self):
        """
        It displays prompt imputs to receive the data from the user.
        """
        print('You\'re about to create an admin user: ')
        email = input('Please, inform an valid user email: ')
        username = input('Please, inform an valid username: ')
        password = input('Please, inform an password: ')
        confirmed_password = input('Please, confirm the password: ')
        
        if not password == confirmed_password:
            raise ValueError('password and password confirmation needs to be equal.')
        
        return {
            'email': email,
            'username': username,
            'password': self.bcrypt_context.hash(password),
            'created_at': datetime.now()
        }

    def execute(self):
        """
        It creates the admin user in the context DB.
        """
        user_data = self.__receive_data()
        user = User(**user_data)
        self.db_session.add(user)
        self.db_session.commit()
        print('Admin user created successfully!')
    
    