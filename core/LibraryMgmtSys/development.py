import environ

from .base import *

env = environ.Env()
environ.Env.read_env("core/LibraryMgmtSys/.env.development")

DEBUG = env.bool("DEBUG", default=False)
SECRET_KEY = env.str("SECRET_KEY")
DATABASES = {"default": env.db("DATABASE_URL")}
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
