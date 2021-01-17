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
        print('this is img idx:', request.form['img_idx'])
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
        myself = (userID == int(request.cookies['userID']))
        follow = False
        infos = get_weibo_info_from_userid(userID)
        infos['img_idx'] = '1'
        posts = get_posts_from_userid(userID)
        posts = get_praise_infos(userID, posts)
        username = request.cookies['username']
        return render_template("profile.html", username=username, myself=myself, follow=follow, infos=infos, posts=posts, title='个人主页')
    except KeyError:
        print(KeyError, " keyerror for username")
        return redirect('/')


@app.route("/edit_profile", methods=['POST','GET'])
def edit_profile():
    error = None
    try:
        userID = int(request.cookies["userID"])
        infos = get_edit_info_from_userid(userID)
        infos['img_idx'] = '3'
        if request.method == 'POST':
            print('editting: ', request.form['img_idx'])
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
        return redirect('/searchresult/%s' % searching)
    try:
        myUserID = int(request.cookies['userID'])
        username = request.cookies["username"]
        results = search_user_in_db(searching)
        results = get_follow_status(myUserID, results)
        return render_template("searchresult.html", username=username, searching=searching, users=results, title='搜索结果')
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
            myUserID = int(request.cookies['userID'])
            if userID == 0:
                userID = myUserID
            myself = (userID == myUserID)
            follow = False
            infos = get_weibo_info_from_userid(userID)
            infos['img_idx'] = '1'
            followings = get_following_from_userid(userID)
            followings = get_follow_status(myUserID, followings)
            username = request.cookies['username']
            return render_template("followings.html", username=username, myself=myself, follow=follow, infos=infos, users=followings, title='关注列表')
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
            myUserID = int(request.cookies['userID'])
            if userID == 0:
                userID = myUserID
            myself = (userID == myUserID)
            follow = True
            infos = get_weibo_info_from_userid(userID)
            infos['img_idx'] = '1'
            followers = get_follower_from_userid(userID)
            followers = get_follow_status(myUserID, followers)
            username = request.cookies['username']
            return render_template("followers.html", username=username, myself=myself, follow=follow, infos=infos, users=followers, title='粉丝列表')
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
            userID = int(request.cookies['userID'])
            username = request.cookies["username"]
            posts = get_all_posts_from_userid(userID)
            posts = get_praise_infos(userID, posts)
            print(posts)
            return render_template("square.html", username=username, posts=posts, title='广场大厅')
    except KeyError:
        print(KeyError, " keyerror for username")
        return redirect('/')


@app.route('/recommends', methods=['POST', 'GET'])
def recommends():
    try:
        if request.method == 'POST':
            searching = request.form['searching']
            return redirect('/searchresult/%s' % searching)
        else:
            userID = int(request.cookies['userID'])
            username = request.cookies["username"]
            posts = get_all_host_posts(userID)
            posts = get_praise_infos(userID, posts)
            print(posts)
            return render_template("recommends.html", username=username, posts=posts, title='热点推荐')
    except KeyError:
        print(KeyError, " keyerror for username")
        return redirect('/')


@app.route('/adsearch', methods=['GET', 'POST'])
def adsearch():
    if request.method == 'POST' and 'searching' in request.form:
        searching = request.form['searching']
        return redirect('/searchresult/%s' % searching)
    error = None
    try:
        userID = int(request.cookies["userID"])
        username = request.cookies["username"]
        if request.method == 'POST':
            infos, error = get_adsearch_result(userID, request)
            infos['img_idx'] = '1'
            if error:
                return render_template("adsearch.html", error=error)
            else:
                return render_template("adsearchresult.html", title='高级搜索结果', username=username, infos=infos)
        return render_template("adsearch.html", error=error)
    except KeyError:
        print(KeyError, " keyerror for username")
        return redirect('/')


@app.route('/follow', methods=['POST'])
def follow():
    follow_id = request.form['follow']
    print('follow id:', follow_id)
    return redirect(request.form['path'])


@app.route('/unfollow', methods=['POST'])
def unfollow():
    unfollow_id = request.form['unfollow']
    print('unfollow id:', unfollow_id)
    return redirect(request.form['path'])


@app.route('/delete_post', methods=['POST'])
def delete_post():
    print('delete post', request.form['postID'])
    return redirect(request.form['path'])


@app.route('/add_post', methods=['POST'])
def add_post():
    text = request.form['content']
    print('Add post: ', text)
    return redirect(request.form['path'])


@app.route('/add_praise', methods=['POST'])
def add_praise():
    print('add praise', request.form['postID'])
    return redirect(request.form['path'])


@app.route('/delete_praise', methods=['POST'])
def delete_praise():
    print('delete praise', request.form['postID'])
    return redirect(request.form['path'])


@app.route('/forward_post', methods=['POST'])
def forward_post():
    print('forward post', request.form['postid'])
    print('new text', request.form['forward_text'])
    return redirect(request.form['path'])


@app.route('/add_reply', methods=['POST'])
def add_reply():
    print('add reply:', request.form['reply_text'])
    print('to: ', request.form['postid'])
    return redirect(request.form['path'])


@app.route('/delete_reply', methods=['POST'])
def delete_reply():
    print('delete reply', request.form['replyID'])
    return redirect(request.form['path'])



if __name__ == "__main__":
    app.run()
