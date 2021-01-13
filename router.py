from flask import *
from utils import *

app = Flask(__name__)

@app.route("/")
def homepage():
    resp = make_response(render_template("homepage.html"))
    resp.set_cookie('username', '', max_age=0)
    resp.set_cookie('userID', '', max_age=0)
    return resp

@app.route("/login", methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        userId, error = valid_login(request.form['account'], request.form['password'])
        # if not error:
        #     resp = make_response(redirect('/sections'))
        #     resp.set_cookie('username', request.form['account'], max_age=3600)
        #     resp.set_cookie('userID', str(userID), max_age=3600)
        #     resp.set_cookie('is_admin', str(is_admin), max_age=3600)
        #     resp.set_cookie('is_master', str(','.join(is_master)), max_age=3600)
        #     return resp
    return render_template("login.html", error=error)

@app.route("/register", methods=['POST', 'GET'])
def register():
    error = None
    if request.method == 'POST':
        userID, error = valid_register(request)
        # if not error:
        #     resp = make_response(redirect('/sections'))
        #     resp.set_cookie('username', request.form['username'], max_age=3600)
        #     resp.set_cookie('userID', str(userID), max_age=3600)
        #     resp.set_cookie('is_admin', 'false', max_age=3600)
        #     resp.set_cookie('is_master', '', max_age=3600)
        #     return resp
    return render_template("register.html", error=error)


if __name__ == "__main__":
    app.run()
