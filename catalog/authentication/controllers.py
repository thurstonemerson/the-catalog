from flask import Blueprint, request, jsonify, g
import jwt, json, requests
from datetime import datetime, timedelta

from functools import wraps
from urlparse import parse_qsl 
from requests_oauthlib import OAuth1
from jwt import DecodeError, ExpiredSignature

# Import the database object from the main app module
from catalog.core import db
from catalog import app

# Define the blueprint: 'auth', set its url prefix: app.url/auth
authentication = Blueprint('auth', __name__, url_prefix='/auth')

# Import module models (i.e. User)
from catalog.authentication.models import User


def create_token(user):
    payload = {
        'sub': user.id,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(days=14)
    }
    token = jwt.encode(payload, app.config['TOKEN_SECRET'])
    return token.decode('unicode_escape')


def parse_token(req):
    token = req.headers.get('Authorization').split()[1]
    return jwt.decode(token, app.config['TOKEN_SECRET'])


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.headers.get('Authorization'):
            response = jsonify(message='Missing authorization header')
            response.status_code = 401
            return response

        try:
            payload = parse_token(request)
        except DecodeError:
            response = jsonify(message='Token is invalid')
            response.status_code = 401
            return response
        except ExpiredSignature:
            response = jsonify(message='Token has expired')
            response.status_code = 401
            return response

        g.user_id = payload['sub']

        return f(*args, **kwargs)

    return decorated_function


# Routes

@authentication.route('/me/JSON')
@login_required
def me():
    user = User.query.filter_by(id=g.user_id).first()
    return jsonify(user.to_json())


@authentication.route('/login', methods=['POST'])
def login():
    user = User.query.filter_by(email=request.json['email']).first()
    if not user or not user.check_password(request.json['password']):
        response = jsonify(message='Wrong Email or Password')
        response.status_code = 401
        return response
    token = create_token(user)
    return jsonify(token=token)


@authentication.route('/signup', methods=['POST'])
def signup():
    user = User(email=request.json['email'], password=request.json['password'])
    db.session.add(user)
    db.session.commit()
    token = create_token(user)
    return jsonify(token=token)



@authentication.route('/facebook', methods=['POST'])
def facebook():
    access_token_url = 'https://graph.facebook.com/v2.3/oauth/access_token'
    graph_api_url = 'https://graph.facebook.com/v2.3/me'

    params = {
        'client_id': request.json['clientId'],
        'redirect_uri': request.json['redirectUri'],
        'client_secret': app.config['FACEBOOK_SECRET'],
        'code': request.json['code']
    }

    # Step 1. Exchange authorization code for access token.
    r = requests.get(access_token_url, params=params) 
    access_token = dict(parse_qsl(r.text))

    # Step 2. Retrieve information about the current user.
    r = requests.get(graph_api_url, params=access_token)
    profile = json.loads(r.text)
    
    print profile

    # Step 3. (optional) Link accounts.
    if request.headers.get('Authorization'):
        user = User.query.filter_by(facebook=profile['id']).first()
        if user:
            response = jsonify(message='There is already a Facebook account that belongs to you')
            response.status_code = 409
            return response

        payload = parse_token(request)

        user = User.query.filter_by(id=payload['sub']).first()
        if not user:
            response = jsonify(message='User not found')
            response.status_code = 400
            return response

        u = User(facebook=profile['id'], display_name=profile['name'])
        db.session.add(u)
        db.session.commit()
        token = create_token(u)
        return jsonify(token=token)

    # Step 4. Create a new account or return an existing one.
    user = User.query.filter_by(facebook=profile['id']).first()
    if user:
        token = create_token(user)
        return jsonify(token=token)

    u = User(facebook=profile['id'], display_name=profile['name'])
    db.session.add(u)
    db.session.commit()
    token = create_token(u)
    return jsonify(token=token)




@authentication.route('/google', methods=['POST'])
def google():
    access_token_url = 'https://accounts.google.com/o/oauth2/token'
    people_api_url = 'https://www.googleapis.com/plus/v1/people/me/openIdConnect'

    payload = dict(client_id=request.json['clientId'],
                   redirect_uri=request.json['redirectUri'],
                   client_secret=app.config['GOOGLE_SECRET'],
                   code=request.json['code'],
                   grant_type='authorization_code')

    # Step 1. Exchange authorization code for access token.
    r = requests.post(access_token_url, data=payload)
    token = json.loads(r.text)
    headers = {'Authorization': 'Bearer {0}'.format(token['access_token'])}

    # Step 2. Retrieve information about the current user.
    r = requests.get(people_api_url, headers=headers)
    profile = json.loads(r.text)

    user = User.query.filter_by(google=profile['sub']).first()
    if user:
        token = create_token(user)
        return jsonify(token=token)
    u = User(google=profile['sub'],
             display_name=profile['name'])
    db.session.add(u)
    db.session.commit()
    token = create_token(u)
    return jsonify(token=token)


@authentication.route('/twitter', methods=['POST'])
def twitter():
    request_token_url = 'https://api.twitter.com/oauth/request_token'
    access_token_url = 'https://api.twitter.com/oauth/access_token'

    if request.json.get('oauth_token') and request.json.get('oauth_verifier'):
        auth = OAuth1(app.config['TWITTER_CONSUMER_KEY'],
                      client_secret=app.config['TWITTER_CONSUMER_SECRET'],
                      resource_owner_key=request.json.get('oauth_token'),
                      verifier=request.json.get('oauth_verifier'))
        r = requests.post(access_token_url, auth=auth)
        profile = dict(parse_qsl(r.text))
        
        user = User.query.filter_by(twitter=profile['user_id']).first()
        if user:
            token = create_token(user)
            return jsonify(token=token)
        u = User(twitter=profile['user_id'],
                 display_name=profile['screen_name'])
        db.session.add(u)
        db.session.commit()
        token = create_token(u)
        return jsonify(token=token)
    else:
        oauth = OAuth1(app.config['TWITTER_CONSUMER_KEY'],
                       client_secret=app.config['TWITTER_CONSUMER_SECRET'],
                       callback_uri=app.config['TWITTER_CALLBACK_URL'])
        r = requests.post(request_token_url, auth=oauth)
        oauth_token = dict(parse_qsl(r.text))
        return jsonify(oauth_token)
    
