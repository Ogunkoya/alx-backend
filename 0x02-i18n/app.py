#!/usr/bin/env python3
import datetime

@app.route('/')
def index():
    if g.user:
        welcome_message = gettext('logged_in_as') % {'username': g.user['name']}
    else:
        welcome_message = gettext('not_logged_in')
    
    current_time = datetime.datetime.now(pytz.timezone(get_timezone()))
    formatted_time = current_time.strftime('%b %d, %Y, %I:%M:%S %p')
    
    return render_template('index.html', welcome_message=welcome_message, current_time=formatted_time)