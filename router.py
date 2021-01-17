from flask import *
import backend as bc

app = Flask(__name__)

@app.route("/")
def homepage():
    resp = make_response(render_template("homepage.html"))
    resp.set_cookie('username', '', max_age=0)
    resp.set_cookie('userID', '', max_age=0)
    return resp

@app.route("/login", methods=['POST', 'GET'])
def login():
    info = None
    if request.method == 'POST':
        ok, info = bc.login(request.form['email'], request.form['password'])
        if ok:
            username = bc.user_query_value(info, 'screen_name')
            resp = make_response(redirect('/square'))
            resp.set_cookie('username', username, max_age=3600)
            resp.set_cookie('userID', info, max_age=3600)
            return resp
    return render_template("login.html", error=info)

@app.route("/register", methods=['POST', 'GET'])
def register():
    info = None
    if request.method == 'POST':
        pwd = request.form['password']
        if pwd != request.form['rpassword']:
            ok = False
            info = '密码不一致'
        else:
            ok, info = bc.register(request.form['email'], request.form['username'], pwd, request.form['img_idx'])
        if ok:
            resp = make_response(redirect('/square'))
            resp.set_cookie('username', request.form['username'], max_age=3600)
            resp.set_cookie('userID', info, max_age=3600)
            return resp
    return render_template("register.html", error=info)


@app.route("/profile", methods=['POST', 'GET'])
@app.route("/profile/<int:userID>", methods=['POST', 'GET'])
def show_profile(userID=0):
    try:
        if request.method == 'POST':
            searching = request.form['searching']
            return redirect('/searchresult/%s' % searching)
        if userID == 0: userID = int(request.cookies['userID'])
        myuid = request.cookies['userID']
        myself = (userID == int(myuid))
        follow = bc.is_following(str(myuid), str(userID))
        infos = bc.genUserInfo(userID)
        posts = [bc.genWeibo(wid, myuid) for wid in bc.user_weibo(str(userID))]
        username = request.cookies['username']
        return render_template("profile.html", username=username, myself=myself, follow=follow, infos=infos, posts=posts, title='个人主页')
    except KeyError:
        print(KeyError, " keyerror for username")
        return redirect('/')

@app.route("/edit_profile", methods=['POST','GET'])
def edit_profile():
    try:
        info = None
        userID = int(request.cookies["userID"])
        infos = bc.genUserInfoEdit(userID)
        if request.method == 'POST':
            userID = int(request.cookies["userID"])
            pwd = request.form['password']
            if pwd != request.form['rpassword']:
                ok = False
                info = '密码不一致'
            else:
                g = request.form['gender']
                if g == '女':
                    gender = 'f'
                elif g == '男':
                    gender = 'm'
                else:
                    gender = '其他'
                # uid, email, screen_name, password, location, url, gender
                ok, info = bc.update_info(str(userID), request.form['email'], request.form['name'], pwd,
                                          request.form['location'], gender, request.form['img_idx'])
            if not ok:
                return render_template("edit_profile.html", infos=infos, error=info)
            else:
                resp = make_response(redirect('/profile/%s' % userID))
                resp.set_cookie('username', request.form['name'], max_age=3600)
                return resp
        return render_template("edit_profile.html", infos=infos, error=info)
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
        myUserID = str(request.cookies['userID'])
        username = request.cookies["username"]
        results = bc.genSearch(searching, myUserID)
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
            follow = bc.is_following(str(myUserID), str(userID))
            infos = bc.genUserInfo(userID)
            followings = bc.genFollowings(userID, myUserID)
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
            follow = bc.is_following(str(myUserID), str(userID))
            infos = bc.genUserInfo(userID)
            followers = bc.genFollowers(userID, myUserID)
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
            posts = [bc.genWeibo(wid, userID) for wid in bc.latest_weibo(str(userID))]
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
            posts = [bc.genWeibo(wid, userID) for wid in bc.all_weibo()]
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
            ok1, uid1 = bc.find_user(request.form['user1'])
            ok2, uid2 = bc.find_user(request.form['user2'])
            if not ok1 or not ok2:
                return render_template("adsearch.html", error='用户不存在')
            result = bc.routes4(uid1, uid2)
            infos = {}
            info_keys = set()
            for r in result:
                cnt = len(r)
                re = tuple([bc.genUserInfo(uid) for uid in r])
                if cnt in info_keys:
                    infos[cnt].append(re)
                else:
                    info_keys.add(cnt)
                    infos[cnt] = [re]
            return render_template("adsearchresult.html", title='高级搜索结果', username=username, infos=infos)
        return render_template("adsearch.html", error=error)
    except KeyError:
        print(KeyError, " keyerror for username")
        return redirect('/')


@app.route('/follow', methods=['POST'])
def follow():
    follow_id = request.form['follow']
    uid = request.cookies["userID"]
    follow_id = str(follow_id)
    if not bc.is_following(uid, follow_id):
        bc.follow(uid, follow_id)
    return redirect(request.form['path'])


@app.route('/unfollow', methods=['POST'])
def unfollow():
    unfollow_id = request.form['unfollow']
    uid = request.cookies["userID"]
    unfollow_id = str(unfollow_id)
    if bc.is_following(uid, unfollow_id):
        bc.unfollow(uid, unfollow_id)
    return redirect(request.form['path'])


@app.route('/delete_post', methods=['POST'])
def delete_post():
    wid = request.form['postID']
    wid = str(wid)
    if bc.weibo_exists(wid):
        bc.delete_weibo(wid)
    return redirect(request.form['path'])


@app.route('/add_post', methods=['POST'])
def add_post():
    text = request.form['content']
    topic, text = bc.genTopicText(text)
    uid = request.cookies["userID"]
    _ = bc.send_weibo(uid, text, topic)
    return redirect(request.form['path'])


@app.route('/add_praise', methods=['POST'])
def add_praise():
    wid = request.form['postID']
    uid = request.cookies["userID"]
    wid = str(wid)
    if not bc.is_liked_by(wid, uid):
        bc.like_it(wid, uid)
    return redirect(request.form['path'])


@app.route('/delete_praise', methods=['POST'])
def delete_praise():
    wid = request.form['postID']
    uid = request.cookies["userID"]
    wid = str(wid)
    if bc.is_liked_by(wid, uid):
        bc.cancel_like_it(wid, uid)
    return redirect(request.form['path'])


@app.route('/forward_post', methods=['POST'])
def forward_post():
    text = request.form['forward_text']
    topic, text = bc.genTopicText(text)
    uid = request.cookies["userID"]
    wid1 = bc.send_weibo(uid, text, topic)
    wid2 = request.form['postid']
    bc.repost_weibo(wid1, wid2)
    return redirect(request.form['path'])


@app.route('/add_reply', methods=['POST'])
def add_reply():
    wid = str(request.form['postid'])
    uid = request.cookies["userID"]
    text = request.form['reply_text']
    _ = bc.send_reply(wid, uid, text)
    return redirect(request.form['path'])


@app.route('/delete_reply', methods=['POST'])
def delete_reply():
    cid = str(request.form['replyID'])
    bc.delete_reply(cid)
    return redirect(request.form['path'])



if __name__ == "__main__":
    app.run()
