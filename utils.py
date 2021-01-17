
# -*- coding: utf-8 -*-
from structs import *

import random

# TODO: finish register check and userID and error message
def valid_register(email, username, password, rpassword):
    error = None
    userID = 0
    # other information?
    # checking...
    # 测试以下内容：邮箱是否已经注册（返回已经注册blabla）
    # userID就是uid，返回时用于保存在cookie，后续拿信息都用这个拿
    # 新用户插入到数据库
    error = 'test'
    return userID, error

# TODO: finish login check and return userID and error message
def valid_login(email, password):
    # 测试邮箱是否已注册、密码是否正确，若有错误则error不为空
    userID = 0
    username = 'test'
    error = None
    return userID, username, error


# TODO: return user information according to user id
def get_weibo_info_from_userid(userID):
    infos = {
        'userID': userID,
        'name': '张三',
        'location': '北京海淀',
        'gender': '男',
        'followersum': 123,
        'friendsum': 1234,
        'statusesum': 12345,
        'created_at': '2020年1月2日',
    }
    return infos


# TODO: return user information according to user id
def get_edit_info_from_userid(userID):
    infos = {
        'name': '张三',
        'email': '123@qq.com',
        'url': '',
        'location': '北京海淀',
        'gender': '男',
    }
    return infos


# TODO: return user posts accordingto user id
def get_posts_from_userid(userID):
    weibo1 = Weibo(0, 1, '@test1', '今天天气真好啊啊啊啊啊啊啊啊啊啊啊啊今天天气真好啊啊啊啊啊啊啊啊啊啊啊啊今天天气真好啊啊啊啊啊啊啊啊啊啊啊啊今天天气真好啊啊啊啊啊啊啊啊啊啊啊啊今天天气真好啊啊啊啊啊啊啊啊啊啊啊啊今天天气真好啊啊啊啊啊啊啊啊啊啊啊啊今天天气真好啊啊啊啊啊啊啊啊啊啊啊啊今天天气真好啊啊啊啊啊啊啊啊啊啊啊啊今天天气真好啊啊啊啊啊啊啊啊啊啊啊啊今天天气真好啊啊啊啊啊啊啊啊啊啊啊啊今天天气真好啊啊啊啊啊啊啊啊啊啊啊啊今天天气真好啊啊啊啊啊啊啊啊啊啊啊啊今天天气真好啊啊啊啊啊啊啊啊啊啊啊啊今天天气真好啊啊啊啊啊啊啊啊啊啊啊啊今天天气真好啊啊啊啊啊啊啊啊啊啊啊啊今天天气真好啊啊啊啊啊啊啊啊啊啊啊啊今天天气真好啊啊啊啊啊啊啊啊啊啊啊啊今天天气真好啊啊啊啊啊啊啊啊啊啊啊啊今天天气真好啊啊啊啊啊啊啊啊啊啊啊啊今天天气真好啊啊啊啊啊啊啊啊啊啊啊啊今天天气真好啊啊啊啊啊啊啊啊啊啊啊啊', '2020年1月1日13:45', 1, 2, 3, '#天气#', [(1, 'test2', '#感想#', '不错'), (1, '@test3', '#感想#', '不错'), (1, '@test4', '#感想#', '不错')], 'test2：#感想# 不错 // @test3：#感想# 不错 // @test4：#感想# 不错 // ', [Reply(12, 3, 'test2', 'good', '2020年1月1日13:46', True)])
    weibo2 = Weibo(2, 2, 'test3', '今天天气真差', '2020年1月1日13:47', 5, 6, 7, '#天气#', [], '', [
        Reply(13, 4, 'test4', 'bad', '2020年1月1日13:48', False),
        Reply(14, 5, 'test5', 'not bad', '2020年1月1日13:49', True),
        ])
    posts = [weibo1, weibo2]
    return posts


# TODO: return all visible posts from user id
def get_all_posts_from_userid(userID):
    weibo1 = Weibo(1, 3, 'test1', '今天天气真好', '2020年1月1日13:45', 1, 2, 3, '#天气#', [], '', [Reply(15, 3, 'test2', 'good', '2020年1月1日13:46', False)])
    weibo2 = Weibo(2, 4, '@test3', '今天天气真差', '2020年1月1日13:47', 5, 6, 7, '#天气#', [(1, 'test2','#感想#', '不错'), (1, '@test3','#感想#', '不错'), (1, '@test4','#感想#', '不错')], 'test2：#感想# 不错 // @test3：#感想# 不错 // @test4：#感想# 不错 // ', [
        Reply(16, 4, 'test4', 'bad', '2020年1月1日13:48', True),
        Reply(17, 5, 'test5', 'not bad', '2020年1月1日13:49', False),
        ])
    posts = [weibo1, weibo2]
    return posts


# TODO: get all hot posts
def get_all_host_posts(userID):
    weibo1 = Weibo(1, 5, 'test1', '今天天气真好', '2020年1月1日13:45', 1, 2, 3, '#天气#', [], '', [Reply(18, 3, 'test2', 'good', '2020年1月1日13:46', True)])
    weibo2 = Weibo(2, 6, '@test3', '今天天气真差', '2020年1月1日13:47', 5, 6, 7, '#天气#', [(1, 'test2', '#感想#', '不错'), (1, '@test3', '#感想#', '不错'), (1, '@test4', '#感想#', '不错')], 'test2：#感想# 不错 // @test3：#感想# 不错 // @test4：#感想# 不错 // ', [
        Reply(19, 4, 'test4', '不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错不错', '2020年1月1日13:48', False),
        Reply(20, 5, 'test5', 'not bad', '2020年1月1日13:49', True),
        ])
    posts = [weibo1, weibo2]
    return posts


# TODO: update informations for users
def update_infos(userID, request):
    print(
        request.form['email'],
        request.form['name'],
        request.form['url'],
        request.form['location'],
        request.form['gender'],
        request.form['password'],
        request.form['rpassword']
    )
    error = None
    error = 'test'
    return error


# TODO: searching
def search_user_in_db(searching):
    results = [
        {
            'userID': 1,
            'name': 'test1',
            'gender': '男',
            'location': '湖北省武汉市江汉区',
            'created_at': '2020年2月2日12:13',
            'followersum': 123,
            'friendsum': 1234,
            'statusesum': 12345,
        },
        {
            'userID': 2,
            'name': 'test2',
            'gender': '女',
            'location': '湖北省武汉市汉阳区',
            'created_at': '2020年2月2日12:12',
            'followersum': 123,
            'friendsum': 1234,
            'statusesum': 12345,
        },
    ]
    return results


# TODO: get following
def get_following_from_userid(userID):
    following = [
        {
            'userID': 0,
            'name': 'test1',
            'gender': '男',
            'location': '湖北省武汉市江汉区',
            'created_at': '2020年2月2日12:13',
            'followersum': 123,
            'friendsum': 1234,
            'statusesum': 12345,
        },
        {
            'userID': 2,
            'name': 'test2',
            'gender': '女',
            'location': '湖北省武汉市汉阳区',
            'created_at': '2020年2月2日12:12',
            'followersum': 123,
            'friendsum': 1234,
            'statusesum': 12345,
        },
    ]
    return following


# TODO: get following
def get_follower_from_userid(userID):
    followers = [
        {
            'userID': 1,
            'name': 'test1',
            'gender': '男',
            'location': '湖北省武汉市江汉区',
            'created_at': '2020年2月2日12:13',
            'followersum': 123,
            'friendsum': 1234,
            'statusesum': 12345,
        },
        {
            'userID': 2,
            'name': 'test2',
            'gender': '女',
            'location': '湖北省武汉市汉阳区',
            'created_at': '2020年2月2日12:12',
            'followersum': 123,
            'friendsum': 1234,
            'statusesum': 12345,
        },
    ]
    return followers


def random_ph_search():
    cands = [
        '如何看待xxx？',
        '#今日热搜#',
        '如何做到xxx？',
        'xxx是一种怎样的体验？',
    ]
    ind = random.randint(0, 3)
    return cands[ind]


# TODO: adsearch result
def get_adsearch_result(userID, request):
    user1 = request.form['user1']
    user2 = request.form['user2']
    error = None
    infos = {
        2: [
            ({
            'userID': 1,
            'name': 'test1',
            'gender': '男',
            'location': '湖北省武汉市江汉区',
            'created_at': '2020年2月2日12:13',
            'followersum': 123,
            'friendsum': 1234,
            'statusesum': 12345,
        },
        {
            'userID': 1,
            'name': 'test2',
            'gender': '女',
            'location': '湖北省武汉市汉阳区',
            'created_at': '2020年2月2日12:12',
            'followersum': 123,
            'friendsum': 1234,
            'statusesum': 12345,
        },)
        ],
        3: [
            ({
            'userID': 1,
            'name': 'test1',
            'gender': '男',
            'location': '湖北省武汉市江汉区',
            'created_at': '2020年2月2日12:13',
            'followersum': 123,
            'friendsum': 1234,
            'statusesum': 12345,
        },
        {
            'userID': 1,
            'name': 'test2',
            'gender': '女',
            'location': '湖北省武汉市汉阳区',
            'created_at': '2020年2月2日12:12',
            'followersum': 123,
            'friendsum': 1234,
            'statusesum': 12345,
        },
        {
            'userID': 1,
            'name': 'test2',
            'gender': '女',
            'location': '湖北省武汉市汉阳区',
            'created_at': '2020年2月2日12:12',
            'followersum': 123,
            'friendsum': 1234,
            'statusesum': 12345,
        })
        ],
        4: [
            ({
            'userID': 1,
            'name': 'test2',
            'gender': '女',
            'location': '湖北省武汉市汉阳区',
            'created_at': '2020年2月2日12:12',
            'followersum': 123,
            'friendsum': 1234,
            'statusesum': 12345,
        },
        {
            'userID': 1,
            'name': 'test2',
            'gender': '女',
            'location': '湖北省武汉市汉阳区',
            'created_at': '2020年2月2日12:12',
            'followersum': 123,
            'friendsum': 1234,
            'statusesum': 12345,
        },{
            'userID': 1,
            'name': 'test2',
            'gender': '女',
            'location': '湖北省武汉市汉阳区',
            'created_at': '2020年2月2日12:12',
            'followersum': 123,
            'friendsum': 1234,
            'statusesum': 12345,
        },{
            'userID': 1,
            'name': 'test2',
            'gender': '女',
            'location': '湖北省武汉市汉阳区',
            'created_at': '2020年2月2日12:12',
            'followersum': 123,
            'friendsum': 1234,
            'statusesum': 12345,
        })
        ],
        5: [
            ({
            'userID': 1,
            'name': 'test2',
            'gender': '女',
            'location': '湖北省武汉市汉阳区',
            'created_at': '2020年2月2日12:12',
            'followersum': 123,
            'friendsum': 1234,
            'statusesum': 12345,
        },
        {
            'userID': 1,
            'name': 'test2',
            'gender': '女',
            'location': '湖北省武汉市汉阳区',
            'created_at': '2020年2月2日12:12',
            'followersum': 123,
            'friendsum': 1234,
            'statusesum': 12345,
        },{
            'userID': 1,
            'name': 'test2',
            'gender': '女',
            'location': '湖北省武汉市汉阳区',
            'created_at': '2020年2月2日12:12',
            'followersum': 123,
            'friendsum': 1234,
            'statusesum': 12345,
        },{
            'userID': 1,
            'name': 'test2',
            'gender': '女',
            'location': '湖北省武汉市汉阳区',
            'created_at': '2020年2月2日12:12',
            'followersum': 123,
            'friendsum': 1234,
            'statusesum': 12345,
        },{
            'userID': 1,
            'name': 'test2',
            'gender': '女',
            'location': '湖北省武汉市汉阳区',
            'created_at': '2020年2月2日12:12',
            'followersum': 123,
            'friendsum': 1234,
            'statusesum': 12345,
        })
        ],
    }
    return infos, error


def get_follow_status(userID, otherUsers):
    for i in range(len(otherUsers)):
        otherUsers[i]['following'] = (i % 2 == 0)
        otherUsers[i]['ismyself'] = (userID == otherUsers[i]['userID'])
    print(otherUsers)
    return otherUsers


def get_praise_infos(userID, posts):
    for i in range(len(posts)):
        posts[i].myself = (userID == posts[i].userID)
        posts[i].praised = i % 2 == 0
    return posts
