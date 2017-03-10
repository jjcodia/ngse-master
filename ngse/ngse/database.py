import sqlalchemy
import os
from sqlalchemy.orm import sessionmaker
from setup import setup

def connect(user, password, db, host='localhost', port=5432):
	url = 'postgresql://{}:{}@{}:{}/{}'.format(user, password, host, port, db)

	db = sqlalchemy.create_engine(url, client_encoding='utf8')
	engine = db.connect()
	meta = sqlalchemy.MetaData(bind=engine, reflect=True)

	return db, engine, meta

''' Database setup '''

if 'TRAVIS' in  os.environ:
	db, engine, meta = connect('postgres', '', 'ngsewebsite')
else:
	db, engine, meta = connect('ngse', 'ngse', 'ngsewebsite')
# Base.metadata.create_all(engine)
SessionFactory = sessionmaker(engine)
session = SessionFactory()
# setup(session)