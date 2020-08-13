import os

AWS_BUCKET                 = os.environ.get("AWS_BUCKET")
AWS_KEY                    = os.environ.get("AWS_KEY")
AWS_SECRET                 = os.environ.get("AWS_SECRET")
AWS_LOCATION               = f"http://{AWS_BUCKET}.s3-ap-southeast-1.amazonaws.com/"

G_CLIENT_ID                 = os.environ.get("GOOGLE_CLIENT_ID")
G_CLIENT_SECRET             = os.environ.get("GOOGLE_CLIENT_SECRET")

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or os.urandom(32)


class ProductionConfig(Config):
    DEBUG = False
    ASSETS_DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
    ASSETS_DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    ASSETS_DEBUG = False

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    ASSETS_DEBUG = True
