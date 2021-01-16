
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
        'name': '张三',
        'location': '北京海淀',
        'gender': '男',
        'followersum': 123,
        'friendsum': 1234,
        'statusesum': 12345,
        'favouritesum': 123456,
        'created_at': '2020年1月2日',
    }
    return infos


# TODO: return user information according to user id
def get_edit_info_from_userid(userID):
    infos = {
        'name': '张三',
        'email': '123@qq.com',
        'province': '北京',
        'city': '',
        'location': '海淀',
        'gender': '男',
    }
    return infos


# TODO: return user posts accordingto user id
def get_posts_from_userid(userID):
    weibo1 = Weibo('test1', '今天天气真好', '2020年1月1日13:45', 1, 2, 3, '天气', [Reply('test2', 'good', '2020年1月1日13:46', 4, 'test1')])
    weibo2 = Weibo('test3', '今天天气真差', '2020年1月1日13:47', 5, 6, 7, '天气', [
        Reply('test4', 'bad', '2020年1月1日13:48', 8, 'test3'),
        Reply('test5', 'not bad', '2020年1月1日13:49', 9, 'test5'),
        ])
    posts = [weibo1, weibo2]
    return posts


# TODO: return all visible posts from user id
def get_all_posts_from_userid(userID):
    weibo1 = Weibo('test1', '今天天气真好', '2020年1月1日13:45', 1, 2, 3, '天气', [Reply('test2', 'good', '2020年1月1日13:46', 4, 'test1')])
    weibo2 = Weibo('test3', '今天天气真差', '2020年1月1日13:47', 5, 6, 7, '天气', [
        Reply('test4', 'bad', '2020年1月1日13:48', 8, 'test3'),
        Reply('test5', 'not bad', '2020年1月1日13:49', 9, 'test5'),
        ])
    posts = [weibo1, weibo2]
    return posts


# TODO: get all hot posts
def get_all_host_posts(userID):
    weibo1 = Weibo('test1', '今天天气真好', '2020年1月1日13:45', 1, 2, 3, '天气', [Reply('test2', 'good', '2020年1月1日13:46', 4, 'test1')])
    weibo2 = Weibo('test3', '今天天气真差', '2020年1月1日13:47', 5, 6, 7, '天气', [
        Reply('test4', 'bad', '2020年1月1日13:48', 8, 'test3'),
        Reply('test5', 'not bad', '2020年1月1日13:49', 9, 'test5'),
        ])
    posts = [weibo1, weibo2]
    return posts


# TODO: update informations for users
def update_infos(userID, request):
    print(
        request.form['email'],
        request.form['name'],
        request.form['province'],
        request.form['city'],
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
            'name': 'test1',
            'gender': '男',
            'location': '湖北省武汉市江汉区',
            'created_at': '2020年2月2日12:13',
            'followersum': 123,
            'friendsum': 1234,
            'statusesum': 12345,
            'favouritesum': 123456,
            'inverse': False,
        },
        {
            'name': 'test2',
            'gender': '女',
            'location': '湖北省武汉市汉阳区',
            'created_at': '2020年2月2日12:12',
            'followersum': 123,
            'friendsum': 1234,
            'statusesum': 12345,
            'favouritesum': 123456,
            'inverse': False,
        },
    ]
    return results


# TODO: get following
def get_following_from_userid(userID):
    following = [
        {
            'name': 'test1',
            'gender': '男',
            'location': '湖北省武汉市江汉区',
            'created_at': '2020年2月2日12:13',
            'followersum': 123,
            'friendsum': 1234,
            'statusesum': 12345,
            'favouritesum': 123456,
            'inverse': False,
        },
        {
            'name': 'test2',
            'gender': '女',
            'location': '湖北省武汉市汉阳区',
            'created_at': '2020年2月2日12:12',
            'followersum': 123,
            'friendsum': 1234,
            'statusesum': 12345,
            'favouritesum': 123456,
            'inverse': False,
        },
    ]
    return following


# TODO: get following
def get_follower_from_userid(userID):
    followers = [
        {
            'name': 'test1',
            'gender': '男',
            'location': '湖北省武汉市江汉区',
            'created_at': '2020年2月2日12:13',
            'followersum': 123,
            'friendsum': 1234,
            'statusesum': 12345,
            'favouritesum': 123456,
            'inverse': False,
        },
        {
            'name': 'test2',
            'gender': '女',
            'location': '湖北省武汉市汉阳区',
            'created_at': '2020年2月2日12:12',
            'followersum': 123,
            'friendsum': 1234,
            'statusesum': 12345,
            'favouritesum': 123456,
            'inverse': False,
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
