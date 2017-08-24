'''A module for setting the configuration setting for when the app is on different
modes'''
import os


class Configurations(object):
    '''Parent class for configurations under config.py module'''
    DEBUG=False
    CSRF_ENABLED=True
    SECRET = os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class UnderProduction(Configurations):
    '''Configurations for whent the mode is under production'''
    DEBUG=False
    TESTING=False


class UnderStaging(Configurations):
    '''Configurations for when the mode is staging'''
    DEBUG=True


class UnderTesting(Configurations):
    '''Configurations for when the mode is under testing, whereby a separate test
    database will be used under this mode'''
    TESTING=True
    SQL_ALCHEMY_DATABASE_URI = os.getenv('postgresql://localhost/test_db')
    DEBUG=True


class UnderDevelopment(Configurations):
    '''Configuration for when the mode is development'''
    DEBUG=True


app_configurations = {
    'production': UnderProduction,
    'staging': UnderStaging,
    'testing': UnderTesting,
    'development': UnderDevelopment
}
