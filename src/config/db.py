import os
from sqlmodel import SQLModel, Session, create_engine
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOSTNAME = os.getenv("DB_HOSTNAME")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{DB_NAME}"
print(DB_URL)

class PSQLConfig(object):
    def __init__(self):
        self.db_url = DB_URL
        self.engine = create_engine(self.db_url, echo=True)

    def get_session(self):
        with Session(self.engine) as session:
            yield session

    def get_local_session(self):
        return Session(self.engine)
