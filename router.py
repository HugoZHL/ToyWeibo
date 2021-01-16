from flask import *
from structs import *
import backend as bc

app = Flask(__name__)

def genUserInfo(uid):
    uid = str(uid)
    r = bc.user_query_values(uid, ['screen_name', 'location', 'gender', 'followersnum', 'friendsnum', 'statusesnum', 'created_at'])
    infos = {
        'userID': int(uid),
        'name': r[0],
        'location': r[1],
        'gender': r[2],
        'followersum': int(r[3]),
        'friendsum': int(r[4]),
        'statusesum': int(r[5]),
        'created_at': r[6],
    }
    return infos

def genUserInfo2(infos, myuid):
    myuid = str(myuid)
    uid = str(infos['userID'])
    infos['following'] = bc.is_following(myuid, uid)
    infos['ismyself'] = (myuid == uid)
    return infos

def genUserInfoBad(uid):
    uid = str(uid)
    r = bc.user_query_values(uid, ['screen_name', 'email', 'location', 'gender'])
    infos = {
        'name': r[0],
        'email': r[1],
        'province': '',
        'city': '',
        'location': r[2],
        'gender': r[3],
    }
    return infos

def genWeibo(wid, myuid):
    wid = str(wid)
    myuid = str(myuid)
    uid = bc.weibo_uid(wid)
    username = bc.user_query_value(uid, 'screen_name')
    r = bc.weibo_query_values(wid, ['text', 'date', 'repostsnum', 'commentsnum', 'attitudesnum', 'topic'])
    # (self, userID, postID, username, text, time, repostsum, commentsum, attitudesum, topic, replies)
    # Weibo(0, 1, 'test1', '今天天气真好', '2020年1月1日13:45', 1, 2, 3, '天气', [])
    wb = Weibo(int(uid), int(wid), username, r[0], r[1], int(r[2]), int(r[3]), int(r[4]), r[5], [])
    wb.myself = (myuid == uid)
    wb.praised = bc.is_liked_by(wid, myuid)
    return wb

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
            info = 'Password inconsistent'
        else:
            ok, info = bc.register(request.form['email'], request.form['username'], pwd, '', '', '')
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
        infos = genUserInfo(userID)
        posts = [genWeibo(wid, myuid) for wid in bc.user_weibo(str(userID))]
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
        infos = genUserInfoBad(userID)
        if request.method == 'POST':
            pwd = request.form['password']
            if pwd != request.form['rpassword']:
                ok = False
                info = 'Password inconsistent'
            else:
                # uid, email, screen_name, password, location, url, gender
                ok, info = bc.update_info(str(userID), request['email'], request['name'], pwd, request['location'], '', request['gender'])
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
    try:
        myUserID = str(request.cookies['userID'])
        username = request.cookies["username"]
        ok, info = bc.find_user(searching)
        results = []
        if ok:
            results = [genUserInfo2(genUserInfo(info), myUserID)]
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
            infos = genUserInfo(userID)
            followings = [genUserInfo2(genUserInfo(uid), myUserID) for uid in bc.followings(str(userID))]
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
            infos = genUserInfo(userID)
            followers = [genUserInfo2(genUserInfo(uid), myUserID) for uid in bc.followers(str(userID))]
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
            posts = [genWeibo(wid, userID) for wid in bc.latest_weibo(str(userID))]
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
            posts = [genWeibo(wid, userID) for wid in bc.all_weibo()]
            print(posts)
            return render_template("recommends.html", username=username, posts=posts, title='热点推荐')
    except KeyError:
        print(KeyError, " keyerror for username")
        return redirect('/')


@app.route('/adsearch', methods=['GET', 'POST'])
def adsearch():
    error = None
    try:
        userID = int(request.cookies["userID"])
        username = request.cookies["username"]
        if request.method == 'POST':
            ok1, uid1 = bc.find_user(request.form['email1'])
            ok2, uid2 = bc.find_user(request.form['email2'])
            if not ok1 or not ok2:
                return render_template("adsearch.html", error='User not exist')
            result = bc.routes4(uid1, uid2)
            infos = {}
            info_keys = set()
            for r in result:
                cnt = len(r)
                re = tuple([genUserInfo(uid) for uid in r])
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
    print('follow id:', follow_id)
    uid = request.cookies["userID"]
    follow_id = str(follow_id)
    if not bc.is_following(uid, follow_id):
        bc.follow(uid, follow_id)
    return redirect(request.form['path'])


@app.route('/unfollow', methods=['POST'])
def unfollow():
    unfollow_id = request.form['unfollow']
    print('unfollow id:', unfollow_id)
    uid = request.cookies["userID"]
    unfollow_id = str(unfollow_id)
    if bc.is_following(uid, unfollow_id):
        bc.unfollow(uid, unfollow_id)
    return redirect(request.form['path'])


@app.route('/delete_post', methods=['POST'])
def delete_post():
    wid = request.form['postID']
    print('delete post', wid)
    wid = str(wid)
    if bc.weibo_exists(wid):
        print('I am trying to delete it...')
        bc.delete_weibo(wid)
    return redirect(request.form['path'])


@app.route('/add_post', methods=['POST'])
def add_post():
    text = request.form['content']
    print('Add post: ', text)
    topic = ''
    if text[0] == '#':
        pos = text.find('#', 1)
        if pos > 0:
            topic = text[1:pos]
            text = text[pos+1:]
    uid = request.cookies["userID"]
    bc.send_weibo(uid, text, topic)
    return redirect(request.form['path'])


@app.route('/add_praise', methods=['POST'])
def add_praise():
    wid = request.form['postID']
    print('add praise', wid)
    uid = request.cookies["userID"]
    wid = str(wid)
    if not bc.is_liked_by(wid, uid):
        bc.like_it(wid, uid)
    return redirect(request.form['path'])


@app.route('/delete_praise', methods=['POST'])
def delete_praise():
    wid = request.form['postID']
    print('delete praise', wid)
    uid = request.cookies["userID"]
    wid = str(wid)
    if bc.is_liked_by(wid, uid):
        bc.cancel_like_it(wid, uid)
    return redirect(request.form['path'])


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
