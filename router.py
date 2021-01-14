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
        userID, username, error = valid_login(request.form['email'], request.form['password'])
        if not error:
            resp = make_response(redirect('/profile'))
            resp.set_cookie('username', username, max_age=3600)
            resp.set_cookie('userID', str(userID), max_age=3600)
            return resp
    return render_template("login.html", error=error)

@app.route("/register", methods=['POST', 'GET'])
def register():
    error = None
    if request.method == 'POST':
        userID, error = valid_register(request)
        if not error:
            resp = make_response(redirect('/profile'))
            resp.set_cookie('username', request.form['username'], max_age=3600)
            resp.set_cookie('userID', str(userID), max_age=3600)
            return resp
    return render_template("register.html", error=error)


@app.route("/profile", methods=['POST', 'GET'])
@app.route("/profile/<int:userID>", methods=['POST', 'GET'])
def show_profile(userID=0):
    try:
        if request.method == 'POST':
            searching = request.form['searching']
            return redirect('/searchresult/%s' % searching)
        if userID == 0: userID = int(request.cookies['userID'])
        infos = get_weibo_info_from_userid(userID)
        posts = get_posts_from_userid(userID)
        return render_template("profile.html", username=request.cookies['username'], infos=infos, posts=posts)
    except KeyError:
        print(KeyError, " keyerror for username")
        return redirect('/')


@app.route("/edit_profile", methods=['POST','GET'])
def edit_profile():
    error = None
    try:
        userID = request.cookies["userID"]
        infos = get_id_info_from_userid(userID)
        if request.method == 'POST':
            error = update_infos(request, userID)
            if error:
                return render_template("edit_profile.html", infos=infos, error=error)
            else:
                return redirect('/profile/%s' % userID)
        return render_template("edit_profile.html", infos=infos, error=error)
    except KeyError:
        print(KeyError, " keyerror for username")
        return redirect('/')


@app.route("/searchresult/")
@app.route("/searchresult/<string:searching>", methods=['POST', 'GET'])
def result_page(searching=""):
    if not searching or request.method=='POST':
        searching = request.form['searching']
    try:
        username = request.cookies["username"]
        result = search_in_db(searching)
        return render_template("searchresult.html", username=username, searching=searching, result=result)
    except KeyError:
        print(KeyError, " keyerror for username")
        return redirect('/')


if __name__ == "__main__":
    app.run()
