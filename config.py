import os


class Config:
	BASE_DIR = os.path.abspath(os.path.dirname(__file__))
	CSRF_ENABLED = True
	CSRF_SESSION_KEY = '670288698c6fe75ef17820c968aa9ec695fb2e3f6c3f993e9a9cdde1b68561d2'
	SECRET_KEY = 'c1983b0bcfa5621cb9b840428cc312af465d1a5edae05b466de67c2b1696453d'


class ProdConfig(Config):
	DEBUG = False
	SQLALCHEMY_DATABASE_URI = ...


class DevConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(Config.BASE_DIR, 'shop_app.db')