import os

DEBUG = True
SQLALCHEMY_TRACK_MODIFICATIONS = False

TOKEN_SECRET = os.environ.get('SECRET_KEY') or 'JWT Token Secret String'
FACEBOOK_SECRET = os.environ.get('FACEBOOK_SECRET') or '7d99bd976045110ab7c479589c6a3d01'
GITHUB_SECRET = os.environ.get('GITHUB_SECRET') or 'GitHub Client Secret'
FOURSQUARE_SECRET = os.environ.get('FOURSQUARE_SECRET') or 'Foursquare Client Secret'
GOOGLE_SECRET = os.environ.get('GOOGLE_SECRET') or 'oXhNlDG-ZS4UpX1Cswl10e7u'
LINKEDIN_SECRET = os.environ.get('LINKEDIN_SECRET') or 'LinkedIn Client Secret'
TWITTER_CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY') or 'Twitter Consumer Secret'
TWITTER_CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET') or 'Twitter Consumer Secret'
TWITTER_CALLBACK_URL = os.environ.get('TWITTER_CALLBACK_URL') or 'Twitter Redirect URI'
BITBUCKET_SECRET = os.environ.get('BITBUCKET_SECRET') or 'Bitbucket Client Secret'
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'postgresql://catalog:YLrvke37pa9JR5x7@localhost/thecatalog'