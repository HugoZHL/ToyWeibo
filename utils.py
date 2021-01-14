# 插入、编辑操作都需要锁

# TODO: finish register check and userID and error message
def valid_register(request):
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    rpassword = request.form['rpassword']
    error = ''
    userID = 0
    # other information?
    # checking...
    # 测试以下内容：邮箱是否已经注册（返回已经注册blabla）
    # UserID从1开始，唯一
    # 新用户插入到数据库
    error = 'test'
    
    return userID, error

# TODO: finish login check and return userID and error message
def valid_login(email, password):
    # 测试邮箱是否已注册、密码是否正确
    userID = 0
    username = 'test'
    error = ''
    return userID, username, error


# TODO: return user information according to user id
def get_weibo_info_from_userid(userID):
    infos = {
        'username': 'test',
        'num_weibo': 12,
        'num_following': 11,
        'num_followers': 10,
    }
    return infos


# TODO: return user information according to user id
def get_id_info_from_userid(userID):
    infos = {
        'username': 'test',
        'email': 'test@test.com',
    }
    return infos


# TODO: return user posts accordingto user id
def get_posts_from_userid(userID):
    posts = []
    return posts


def update_infos(request, userID):
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    rpassword = request.form['rpassword']
    error = ''
    error = 'test'
    return error