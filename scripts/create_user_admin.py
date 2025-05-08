from datetime import datetime
from src.v1.models import User
from passlib.context import CryptContext
from src.config.db import PSQLConfig

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def receive_data():
    print("You're about to create an admin user: ")
    email = input("Please, inform an valid user email: ")
    username = input("Please, inform an valid username: ")
    password = input("Please, inform an password: ")
    
    return {
        "email": email,
        "username": username,
        "password": bcrypt_context.hash(password),
        "created_at": datetime.now()
    }

def get_db_session():
    return PSQLConfig().get_local_session()

def create_user():
    session = get_db_session()
    user_data = receive_data()
    user = User(**user_data)
    session.add(user)
    session.commit()
    print("Admin user created successfully!")

if __name__=="__main__":
    create_user()