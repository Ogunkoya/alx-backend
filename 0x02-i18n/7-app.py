#!/usr/bin/env python3
import pytz

from flask import Flask, render_template, request, g
from flask_babel import Babel, gettext

app = Flask(__name__)
babel = Babel(app)

class Config:
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'

app.config.from_object(Config)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

def get_user(user_id):
    return users.get(user_id)

def validate_timezone(timezone):
    try:
        pytz.timezone(timezone)
        return timezone
    except pytz.exceptions.UnknownTimeZoneError:
        return 'UTC'

@babel.localeselector
def get_locale():
    if 'locale' in request.args and request.args.get('locale') in app.config['LANGUAGES']:
        return request.args.get('locale')
    if g.user and g.user['locale'] in app.config['LANGUAGES']:
        return g.user['locale']
    return request.accept_languages.best_match(app.config['LANGUAGES'])

@babel.timezoneselector
def get_timezone():
    if 'timezone' in request.args:
        return validate_timezone(request.args.get('timezone'))
    if g.user and g.user['timezone']:
        return validate_timezone(g.user['timezone'])
    return 'UTC'

@app.before_request
def before_request():
    user_id = request.args.get('login_as')
    g.user = get_user(int(user_id)) if user_id else None

@app.route('/')
def index():
    if g.user:
        welcome_message = gettext('logged_in_as') % {'username': g.user['name']}
    else:
        welcome_message = gettext('not_logged_in')
    return render_template('7-index.html', welcome_message=welcome_message)