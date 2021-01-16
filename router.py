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
            resp = make_response(redirect('/square'))
            resp.set_cookie('username', username, max_age=3600)
            resp.set_cookie('userID', str(userID), max_age=3600)
            return resp
    return render_template("login.html", error=error)

@app.route("/register", methods=['POST', 'GET'])
def register():
    error = None
    if request.method == 'POST':
        userID, error = valid_register(request.form['email'], request.form['username'], request.form['password'], request.form['rpassword'])
        if not error:
            resp = make_response(redirect('/square'))
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
        return render_template("profile.html", username=request.cookies['username'], infos=infos, posts=posts, title='个人主页', ph_search=random_ph_search())
    except KeyError:
        print(KeyError, " keyerror for username")
        return redirect('/')


@app.route("/edit_profile", methods=['POST','GET'])
def edit_profile():
    error = None
    try:
        userID = request.cookies["userID"]
        infos = get_edit_info_from_userid(userID)
        if request.method == 'POST':
            error = update_infos(userID, request)
            if error:
                return render_template("edit_profile.html", infos=infos, error=error)
            else:
                resp = make_response(redirect('/profile/%s' % userID))
                resp.set_cookie('username', request.form['name'], max_age=3600)
                return resp
        return render_template("edit_profile.html", infos=infos, error=error)
    except KeyError:
        print(KeyError, " keyerror for username")
        return redirect('/')


@app.route("/searchresult/", methods=['POST', 'GET'])
@app.route("/searchresult/<string:searching>", methods=['POST', 'GET'])
def result_page(searching=""):
    if not searching or request.method=='POST':
        searching = request.form['searching']
    try:
        username = request.cookies["username"]
        result = search_in_db(searching)
        return render_template("searchresult.html", username=username, searching=searching, result=result, title='搜索结果', ph_search=random_ph_search())
    except KeyError:
        print(KeyError, " keyerror for username")
        return redirect('/')


@app.route("/following", methods=['POST', 'GET'])
@app.route("/following/<int:userID>", methods=['POST', 'GET'])
def show_following(userID=0):
    try:
        if request.method == 'POST':
            searching = request.form['searching']
            return redirect('/searchresult/%s' % searching)
        else:
            username = request.cookies["username"]
            if userID == 0: userID = int(request.cookies['userID'])
            infos = get_weibo_info_from_userid(userID)
            followings = get_following_from_userid(userID)
            return render_template("followings.html", username=username, infos=infos, users=followings, title='关注列表', ph_search=random_ph_search())
    except KeyError:
        print(KeyError, " keyerror for username")
        return redirect('/')


@app.route("/follower", methods=['POST', 'GET'])
@app.route("/follower/<int:userID>", methods=['POST', 'GET'])
def show_follower(userID=0):
    try:
        if request.method == 'POST':
            searching = request.form['searching']
            return redirect('/searchresult/%s' % searching)
        else:
            username = request.cookies["username"]
            if userID == 0: userID = int(request.cookies['userID'])
            infos = get_weibo_info_from_userid(userID)
            followers = get_follower_from_userid(userID)
            print(infos)
            print(followers)
            return render_template("followers.html", username=username, infos=infos, users=followers, title='粉丝列表', ph_search=random_ph_search())
    except KeyError:
        print(KeyError, " keyerror for username")
        return redirect('/')


@app.route('/square', methods=['POST', 'GET'])
def square():
    try:
        if request.method == 'POST':
            searching = request.form['searching']
            return redirect('/searchresult/%s' % searching)
        else:
            userID = request.cookies['userID']
            username = request.cookies["username"]
            posts = get_all_posts_from_userid(userID)
            return render_template("square.html", username=username, posts=posts, title='广场大厅', ph_search=random_ph_search())
    except KeyError:
        print(KeyError, " keyerror for username")
        return redirect('/')


@app.route('/follow', methods=['POST'])
def follow():
    pass


@app.route('/unfollow', methods=['POST'])
def unfollow():
    pass


@app.route('/delete_post', methods=['POST'])
def delete_post():
    pass


@app.route('/add_post', methods=['POST'])
def add_post():
    pass


@app.route('/add_praise', methods=['POST'])
def add_praise():
    pass


@app.route('/delete_praise', methods=['POST'])
def delete_praise():
    pass


@app.route('/forward_post', methods=['POST'])
def forward_post():
    pass


@app.route('/add_reply', methods=['POST'])
def add_reply():
    pass


@app.route('/delete_reply', methods=['POST'])
def delete_reply():
    pass



if __name__ == "__main__":
    app.run()
