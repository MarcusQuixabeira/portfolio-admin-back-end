import os
from sqlmodel import SQLModel, Session, create_engine

DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOSTNAME = os.environ["DB_HOSTNAME"]
BD_PORT = os.environ["BD_PORT"]
DB_NAME = os.environ["DB_NAME"]

class PSQLConfig(object):
    def __init__(self):
        self.db_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOSTNAME}:{BD_PORT}/{DB_NAME}"
        self.engine = create_engine(self.db_url, echo=True)

    def get_session(self):
        with Session(self.engine) as session:
            yield session
    
    def get_local_session(self):
        return Session(self.engine)
