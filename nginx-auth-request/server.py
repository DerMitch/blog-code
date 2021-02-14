import time

import bcrypt
from itsdangerous.url_safe import URLSafeTimedSerializer
from itsdangerous.exc import BadSignature, SignatureExpired

from flask import Flask, render_template, request, make_response

app = Flask(__name__)

serializer = URLSafeTimedSerializer("980b4ab559a51b8531363f70e7f24fb462235f1a")

USERS = {
    # mitch:demo
    'mitch': b'$2b$12$/BOdvK3qy88BJPQgoR3SHup73flz13FfF213byXbWWlUR15YBcpGC',
}

COOKIE_NAME = "_custom_auth_token"
SESSION_LIFETIME = 3600 # seconds

@app.route("/", methods=['GET', 'POST'])
def login():
    """
    A simple login form that sets a cookie with a signed session on success.
    Uses itsdangerous for safely passing values around.
    """
    error = None

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        url = serializer.loads(request.form['url'])

        if pwhash := USERS.get(username):
            if bcrypt.checkpw(password.encode(), pwhash):
                # Give the user a session!

                # redirect() returns a Response object which we can modify
                r = make_response('', 302)
                r.set_cookie(COOKIE_NAME, serializer.dumps(username))
                r.headers['location'] = url
                return r
            else:
                return render_template("login.html", error="Wrong password")
        else:
            return render_template("login.html", error="No such user")
    
    # We URL we sent the user to after the request
    # For additional security, you could whitelist allowed services
    redirect_url = request.args.get('url')
    if not redirect_url:
        error = "Missing redirect URL"

    return render_template("login.html",
        error=error,
        redirect_url=serializer.dumps(redirect_url),
    )


@app.route("/validate", methods=['GET', 'POST'])
def validate():
    """
    The validation endpoint for nginx' auth_request handler.
    Checks if the authentication cookie is valid and not expired yet.
    """
    if token := request.cookies.get(COOKIE_NAME):
        try:
            username = serializer.loads(token, max_age=SESSION_LIFETIME)

            r = make_response("OK", 200)
            r.headers['x-auth-username'] = username
            return r
        except BadSignature as e:
            return "BadSignature", 401
        except SignatureExpired as e:
            return "SignatureExpired", 401
    return "MissingCookie", 401
