
# sudo bin/gbuild toyweibo ../ToyWeibo/sql2rdf/small.nt
# sudo bin/ghttp 9000 toyweibo
# sudo bin/shutdown 9000
# sudo bin/gdrop toyweibo

import GstoreConnector
import json
import time
from structs import *

prefix = {'u':'http://example.org/user/', 
    'w': 'http://example.org/weibo/',
    'c': 'http://example.org/comment/',
    'ua': 'http://example.org/user_attr/',
    'wa': 'http://example.org/weibo_attr/',
    'ca': 'http://example.org/comment_attr/',
    'r': 'http://example.org/rel/'}

database = 'toyweibo'
u_len = len(prefix['u'])
w_len = len(prefix['w'])
c_len = len(prefix['c'])
prefix_string = ''.join(['prefix %s:<%s> ' % (k,v) for k,v in prefix.items()])
gc = GstoreConnector.GstoreConnector('localhost', 9000, 'root', '123456')
_ = gc.load(database)

# def transfer(l):
#     ls = l.split(' ')
#     for lls in ls:
#         for k,v in prefix.items():
#             if lls.startswith(k+':'):
#                 llss = lls.split(':')
#                 uri = '<' + v + llss[1] + '>'
#                 l = l.replace(lls, uri)
#     return l

# basic functions

def handle_bad(ls):
    return [l.replace('\\', '\\\\').replace('\"', '\\\"').replace('\'', '\\\'').replace('\n', '').replace('\r', '') for l in ls]

def handle_bad_r(ls):
    return [l.replace('\\\"', '\"').replace('\\\'', '\'').replace('\\\\', '\\') for l in ls]

def run_sparql(l):
    ret = gc.query(database, 'json', prefix_string + l)
    return ret

def query(l):
    return json.loads(run_sparql(l))['results']['bindings']

def is_unique(key, value):
    data = query('select ?x where { ?x ua:%s \"%s\" }' % (key, value))
    if len(data) == 0:
        return True
    else:
        return False



# user queries

def user_query(uid, k):
    return query('select ?x where { u:%s ua:%s ?x }' % (uid, k))

def user_query_value(uid, k):
    return user_query(uid, k)[0]['x']['value']

def user_query_values(uid, keys):
    sel = ''
    qs = []
    for k in keys:
        sel += '?%s ' % (k)
        qs.append('u:%s ua:%s ?%s' % (uid, k, k))
    q = ' . '.join(qs)
    data = query('select ' + sel + 'where { ' + q + ' }')[0]
    return [data[k]['value'] for k in keys]

def user_query_values_filter(fil, keys, limits):
    sel = '?uid '
    qs = []
    for k in keys:
        sel += '?%s ' % (k)
        qs.append('?uid ua:%s ?%s' % (k, k))
    q = ' . '.join(qs)
    data = query('select ' + sel + 'where { ' + q + ' ' + fil + ' } ' + limits)
    return [[d['uid']['value'][u_len:]] + [d[k]['value'] for k in keys] for d in data]

def user_insert_strings(uid, kv_dict):
    for k,v in kv_dict.items():
        _ = run_sparql('insert data { u:%s ua:%s \"%s\" }' % (uid, k, v))

def user_insert_ints(uid, kv_dict):
    for k,v in kv_dict.items():
        _ = run_sparql('insert data { u:%s ua:%s \"%d\"^^<http://www.w3.org/2001/XMLSchema#integer> }' % (uid, k, v))

def user_delete_strings(uid, keys):
    values = user_query_values(uid, keys)
    for i in range(len(keys)):
        k = keys[i]
        v = values[i]
        _ = run_sparql('delete data { u:%s ua:%s \"%s\" } ' % (uid, k, v))

def user_delete_ints(uid, keys):
    values = user_query_values(uid, keys)
    for i in range(len(keys)):
        k = keys[i]
        v = values[i]
        _ = run_sparql('delete data { u:%s ua:%s \"%s\"^^<http://www.w3.org/2001/XMLSchema#integer> } ' % (uid, k, v))

def user_update_int(uid, k, delta):
    v = int(user_query_value(uid, k))
    v += delta
    user_delete_ints(uid, [k])
    user_insert_ints(uid, {k:v})



# weibo queries

def weibo_query(wid, k):
    return query('select ?x where { w:%s wa:%s ?x }' % (wid, k))

def weibo_query_value(wid, k):
    return weibo_query(wid, k)[0]['x']['value']

def weibo_query_values(wid, keys):
    sel = ''
    qs = []
    for k in keys:
        sel += '?%s ' % (k)
        qs.append('w:%s wa:%s ?%s' % (wid, k, k))
    q = ' . '.join(qs)
    data = query('select ' + sel + 'where { ' + q + ' }')[0]
    return [data[k]['value'] for k in keys]

def weibo_insert_strings(wid, kv_dict):
    for k,v in kv_dict.items():
        _ = run_sparql('insert data { w:%s wa:%s \"%s\" }' % (wid, k, v))

def weibo_insert_ints(wid, kv_dict):
    for k,v in kv_dict.items():
        _ = run_sparql('insert data { w:%s wa:%s \"%d\"^^<http://www.w3.org/2001/XMLSchema#integer> }' % (wid, k, v))

def weibo_delete_strings(wid, keys):
    values = weibo_query_values(wid, keys)
    for i in range(len(keys)):
        k = keys[i]
        v = values[i]
        _ = run_sparql('delete data { w:%s wa:%s \"%s\" } ' % (wid, k, v))

def weibo_delete_ints(wid, keys):
    values = weibo_query_values(wid, keys)
    for i in range(len(keys)):
        k = keys[i]
        v = values[i]
        _ = run_sparql('delete data { w:%s wa:%s \"%s\"^^<http://www.w3.org/2001/XMLSchema#integer> } ' % (wid, k, v))

def weibo_update_int(wid, k, delta):
    v = int(weibo_query_values(wid, [k])[0])
    v += delta
    weibo_delete_ints(wid, [k])
    weibo_insert_ints(wid, {k:v})



# user account management

def register(email, screen_name, password, photo):
    email, screen_name, password, photo = handle_bad([email, screen_name, password, photo])
    if not is_unique('email', email):
        return (False, '该邮箱已被注册')
    if not is_unique('screen_name', screen_name):
        return (False, '该昵称已被注册')
    uid = query('select ?uid where { u:next r:is ?uid }')[0]['uid']['value']
    next_uid = str(int(uid) + 1)
    _ = run_sparql('delete data { u:next r:is \"%s\" }' % (uid))
    _ = run_sparql('insert data { u:next r:is \"%s\" }' % (next_uid))
    user_insert_strings(uid, {'email':email, 'screen_name':screen_name, 'password':password, 'location':'未知地区', 'gender':'', 'photo':photo})
    user_insert_ints(uid, {'followersnum':0, 'friendsnum':0, 'statusesnum':0}) # followers, followings, weibos
    user_insert_strings(uid, {'created_at':time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())})
    gc.checkpoint(database)
    return (True, uid)

def login(email, password):
    email, password = handle_bad([email, password])
    uids = query('select ?uid where { ?uid ua:email \"%s\" . ?uid ua:password \"%s\" }' % (email, password))
    if len(uids) == 0:
        return (False, '邮箱或密码错误，请重新输入。')
    else:
        uid = uids[0]['uid']['value'][u_len:]
        return (True, uid)

# def change_password(uid, old_pwd, new_pwd):
#     old_pwd, new_pwd = handle_bad([old_pwd, new_pwd])
#     if old_pwd != user_query_value(uid, 'password')[0]:
#         return False
#     else:
#         user_delete_values(uid, ['password'])
#         user_insert_strings(uid, {'password': new_pwd})
#         gc.checkpoint(database)
#         return True

def update_info(uid, email, screen_name, password, location, gender, photo):
    email, screen_name, password, location, gender, photo = handle_bad([email, screen_name, password, location, gender, photo])
    cur_email, cur_screen_name = user_query_values(uid, ['email', 'screen_name'])
    if not email == cur_email and not is_unique('email', email):
        return (False, '该邮箱已被注册')
    if not screen_name == cur_screen_name and not is_unique('screen_name', screen_name):
        return (False, '该昵称已被注册')
    user_delete_strings(uid, ['email', 'screen_name', 'password', 'location', 'gender', 'photo'])
    user_insert_strings(uid, {'email':email, 'screen_name':screen_name, 'password':password, 'location':location, 'gender':gender, 'photo':photo})
    gc.checkpoint(database)
    return (True, '修改成功')


# weibo management

def weibo_exists(wid):
    return len(query('select ?d where { w:%s wa:date ?d }' % (wid))) != 0

def weibo_valid(wid):
    return len(query('select ?d where { w:%s wa:repostsnum ?d }' % (wid))) != 0

def weibo_uid(wid):
    return query('select ?uid where { w:%s r:by ?uid }' % (wid))[0]['uid']['value'][u_len:]
    
def send_weibo(uid, text, topic):
    text, topic = handle_bad([text, topic])
    wid = query('select ?wid where { w:next r:is ?wid }')[0]['wid']['value']
    next_wid = str(int(wid) + 1)
    _ = run_sparql('delete data { w:next r:is \"%s\" }' % (wid))
    _ = run_sparql('insert data { w:next r:is \"%s\" }' % (next_wid))
    _ = run_sparql('insert data { w:%s wa:text \"%s\" }' % (wid, text))
    _ = run_sparql('insert data { w:%s wa:topic \"%s\" }' % (wid, topic))
    _ = run_sparql('insert data { w:%s r:by u:%s }' % (wid, uid))
    _ = run_sparql('insert data { w:%s wa:date \"%s\" }' % (wid, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    weibo_insert_ints(wid, {'repostsnum':0, 'commentsnum':0, 'attitudesnum':0})
    user_update_int(uid, 'statusesnum', 1)
    gc.checkpoint(database)
    return wid

def repost_weibo(wid1, wid2):
    _ = run_sparql('insert data { w:%s r:repost w:%s }' % (wid1, wid2))
    weibo_update_int(wid2, 'repostsnum', 1)
    gc.checkpoint(database)

def delete_weibo(wid):
    uid = weibo_uid(wid)
    user_update_int(uid, 'statusesnum', -1)
    wid2_urls = query('select ?wid where { w:%s r:repost ?wid }' % (wid))
    if len(wid2_urls) > 0:
        wid2 = wid2_urls[0]['wid']['value'][w_len:]
        weibo_update_int(wid2, 'repostsnum', -1)
    weibo_delete_strings(wid, ['date', 'topic', 'text'])
    weibo_insert_strings(wid, {'topic':'', 'text':'此微博已删除'})
    gc.checkpoint(database)





# user relations

def find_user(screen_name):
    screen_name = handle_bad([screen_name])[0]
    uid_urls = query('select ?uid where { ?uid ua:screen_name \"%s\" }' % (screen_name))
    if len(uid_urls) == 0:
        return (False, '该用户不存在')
    else:
        return (True, uid_urls[0]['uid']['value'][u_len:])

def followers(uid):
    uid_urls = query('select ?uid where { ?uid r:follow u:%s }' % (uid))
    return [url['uid']['value'][u_len:] for url in uid_urls]

def followings(uid):
    uid_urls = query('select ?uid where { u:%s r:follow ?uid }' % (uid))
    return [url['uid']['value'][u_len:] for url in uid_urls]

def follow(uid1, uid2):
    _ = run_sparql('insert data { u:%s r:follow u:%s }' % (uid1, uid2))
    user_update_int(uid1, 'friendsnum', 1)
    user_update_int(uid2, 'followersnum', 1)

def unfollow(uid1, uid2):
    _ = run_sparql('delete data { u:%s r:follow u:%s }' % (uid1, uid2))
    user_update_int(uid1, 'friendsnum', -1)
    user_update_int(uid2, 'followersnum', -1)

def is_following(uid1, uid2):
    return len(query('select ?r where { u:%s ?r u:%s filter( ?r = r:follow ) }' % (uid1, uid2))) != 0

def routes(uid1, uid2, cnt):
    q = 'select'
    for i in range(cnt):
        q += ' ?x%d' % (i)
    q += ' where { u:%s' % (uid1)
    for i in range(cnt):
        q += ' r:follow ?x%d . ?x%d' % (i, i)
    q += ' r:follow u:%s } limit 50' % (uid2)
    data = query(q)
    ans = []
    for d in data:
        a = [uid1]
        for i in range(cnt):
            a.append(d['x%d' % (i)]['value'][u_len:])
        a.append(uid2)
        ans.append(a)
    return ans

def routes4(uid1, uid2):
    ans = []
    if is_following(uid1, uid2):
        ans.append([uid1, uid2])
    for i in range(3):
        result = routes(uid1, uid2, i+1)
        for r in result:
            if len(set(r)) == len(r):
                ans.append(r)
    return ans

# def nhops(uid, n):
#     q = 'select ?x%d where { u:%s' % (n-1, uid)
#     for i in range(n-1):
#         q += ' r:follow ?x%d . ?x%d' % (i, i)
#     q += ' r:follow ?x%d }' % (n-1)
#     data = query(q)
#     return [d['x%d' % (n-1)]['value'][u_len:] for d in data]
#
# def nhops_all(uid, n):
#     ans = set()
#     for i in range(n):
#         ans.update(nhops(uid, i+1))
#     return list(ans)



# like

def is_liked_by(wid, uid):
    return len(query('select ?uid where { w:%s r:likedby ?uid filter( ?uid = u:%s ) }' % (wid, uid))) != 0

def like_it(wid, uid):
    _ = run_sparql('insert data { w:%s r:likedby u:%s }' % (wid, uid))
    weibo_update_int(wid, 'attitudesnum', 1)
    gc.checkpoint(database)

def cancel_like_it(wid, uid):
    _ = run_sparql('delete data { w:%s r:likedby u:%s }' % (wid, uid))
    weibo_update_int(wid, 'attitudesnum', -1)
    gc.checkpoint(database)



# reply

def weibo_reply(wid):
    ans = []
    cid_urls = query('select ?cid ?uid ?username ?text ?t ?photo where { ?cid r:cto w:%s . ?cid ca:time ?t . ?cid ca:text ?text . ?cid r:cby ?uid . ?uid ua:screen_name ?username . ?uid ua:photo ?photo } order by desc(?t)' % (wid))
    for url in cid_urls:
        # replyID, userID, username, text, time, myself
        cid = url['cid']['value'][c_len:]
        uid = url['uid']['value'][u_len:]
        username = url['username']['value']
        text = url['text']['value']
        t = url['t']['value']
        photo = url['photo']['value']
        ans.append([cid, uid, username, text, t, photo])
    return ans

def send_reply(wid, uid, text):
    text = handle_bad([text])[0]
    cid = query('select ?cid where { c:next r:is ?cid }')[0]['cid']['value']
    next_cid = str(int(cid) + 1)
    _ = run_sparql('delete data { c:next r:is \"%s\" }' % (cid))
    _ = run_sparql('insert data { c:next r:is \"%s\" }' % (next_cid))
    _ = run_sparql('insert data { c:%s ca:text \"%s\" }' % (cid, text))
    _ = run_sparql('insert data { c:%s r:cby u:%s }' % (cid, uid))
    _ = run_sparql('insert data { c:%s r:cto w:%s }' % (cid, wid))
    _ = run_sparql('insert data { c:%s ca:time \"%s\" }' % (cid, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    weibo_update_int(wid, 'commentsnum', 1)
    gc.checkpoint(database)
    return cid

def delete_reply(cid):
    wid = query('select ?wid where { c:%s r:cto ?wid }' % (cid))[0]['wid']['value'][w_len:]
    weibo_update_int(wid, 'commentsnum', -1)
    t = query('select ?t where { c:%s ca:time ?t }' % (cid))[0]['t']['value']
    _ = run_sparql('delete data { c:%s ca:time \"%s\" }' % (cid, t))
    gc.checkpoint(database)




# for test

# def bunch_register(n):
#     for i in range(n):
#         x = str(i+1)
#         register(x,x,x,'','','')
#
# def bunch_follow(n):
#     for i in range(n-1):
#         follow(str(i+1), str(i+2))



# some functions for userInfo

def getUserName(uid):
    return handle_bad_r([user_query_value(uid, 'screen_name')])[0]

def genUserInfoFromR(uid, r):
    if r[2] == 'f':
        gender = '女'
    elif r[2] == 'm':
        gender = '男'
    else:
        gender = '性别未知或其他'
    name, location = handle_bad_r([r[0], r[1]])
    infos = {
        'userID': int(uid),
        'name': name,
        'location': location,
        'gender': gender,
        'followersum': int(r[3]),
        'friendsum': int(r[4]),
        'statusesum': int(r[5]),
        'created_at': r[6],
        'img_idx': r[7],
    }
    return infos

def genUserInfo(uid):
    uid = str(uid)
    r = user_query_values(uid, ['screen_name', 'location', 'gender', 'followersnum', 'friendsnum', 'statusesnum', 'created_at', 'photo'])
    return genUserInfoFromR(uid, r)

# data = query('select ' + sel + 'where { ' + q + ' ' + fil + ' }')
def genUserInfoFilter(fil, myuid, limits):
    myuid = str(myuid)
    myfollows = set(followings(myuid))
    rs = user_query_values_filter(fil, ['screen_name', 'location', 'gender', 'followersnum', 'friendsnum', 'statusesnum', 'created_at', 'photo'], limits)
    all_infos = []
    for r in rs:
        uid = r[0]
        infos = genUserInfoFromR(uid, r[1:])
        infos['following'] = (uid in myfollows)
        infos['ismyself'] = (uid == myuid)
        all_infos.append(infos)
    return all_infos

def genSearch(searching, myuid):
    keywords = searching.split(' ')
    filters = ''
    for w in keywords:
        if w != '':
            filters += 'filter regex(?screen_name, \"%s\" ) ' % (handle_bad([w])[0])
    if not filters:
        return []
    return genUserInfoFilter(filters, myuid, 'limit 1000')

def genFollowings(uid, myuid):
    return genUserInfoFilter('. u:%s r:follow ?uid' % (str(uid)), myuid, '')

def genFollowers(uid, myuid):
    return genUserInfoFilter('. ?uid r:follow u:%s' % (str(uid)), myuid, '')

def genUserInfoEdit(uid):
    uid = str(uid)
    r = user_query_values(uid, ['screen_name', 'email', 'location', 'gender', 'photo'])
    name, email, location = handle_bad_r([r[0], r[1], r[2]])
    if r[3] == 'f':
        gender = '女'
    elif r[3] == 'm':
        gender = '男'
    else:
        gender = ''
    infos = {
        'name': name,
        'email': email,
        'location': location,
        'gender': gender,
        'img_idx': r[4],
    }
    return infos

def genReply(c, myuid):
    myuid = str(myuid)
    myself = (c[1] == myuid)
    username, text = handle_bad_r([c[2], c[3]])
    # replyID, userID, username, text, time, myself, photo
    return Reply(int(c[0]), int(c[1]), username, text, c[4], myself, c[5])



# some functions for Weibo Info

def weibo_info(fil, keys, limits):
    data0 = query('select ?wid ?d where { ?wid wa:date ?d ' + fil + ' } order by desc(?d) ' + limits)
    if len(data0) == 0:
        return []
    mind = data0[-1]['d']['value']
    sel = '?wid ?d ?uid ?username ?photo '
    qs = ['?wid wa:date ?d filter ( ?d >= \"%s\" )' % (mind), '?wid r:by ?uid', '?uid ua:screen_name ?username', '?uid ua:photo ?photo']
    for k in keys:
        sel += '?%s ' % (k)
        qs.append('?wid wa:%s ?%s' % (k, k))
    q = ' . '.join(qs)
    data = query('select ' + sel + 'where { ' + q + ' ' + fil + ' } order by desc(?d) ' + limits)
    # wid, uid, username, photo, date, ...
    return [[d['wid']['value'][w_len:], d['uid']['value'][u_len:], d['username']['value'], d['photo']['value'], d['d']['value']] +
            [d[k]['value'] for k in keys] for d in data]

def weibo_filter(fil, limits):
    wid_urls = query('select distinct ?wid ?d where { ?wid wa:date ?d . ' + fil + ' } order by desc(?d) ' + limits)
    return [url['wid']['value'][w_len:] for url in wid_urls]

def repost_list(wid):
    ans = []
    wid1 = wid
    wid2_urls = query('select ?wid where { w:%s r:repost ?wid }' % (wid1))
    while len(wid2_urls) > 0:
        wid2 = wid2_urls[0]['wid']['value'][w_len:]
        # userID, username, topic, text
        data = query('select ?uid ?username ?topic ?text where { w:%s r:by ?uid . ?uid ua:screen_name ?username . w:%s wa:topic ?topic . w:%s wa:text ?text }' % (wid2, wid2, wid2))
        if len(data) == 0:
            break
        uid = data[0]['uid']['value'][u_len:]
        screen_name = '@' + data[0]['username']['value']
        topic = data[0]['topic']['value']
        text = data[0]['text']['value']
        if topic != '':
            topic = '#' + topic + '#' + ' '
        screen_name, topic, text = handle_bad_r([screen_name, topic, text])
        ans.append((int(uid), screen_name, topic, text))
        wid1 = wid2
        wid2_urls = query('select ?wid where { w:%s r:repost ?wid }' % (wid1))
    return ans

def genWeibosFilter(fil, myuid, limits):
    myuid = str(myuid)
    # wid, uid, username, photo, date, text, repostsnum, commentsnum, attitudesnum, topic
    # 0    1    2         3      4     5     6           7            8             9
    rs = weibo_info(fil, ['text', 'repostsnum', 'commentsnum', 'attitudesnum', 'topic'], limits)
    wid_r = set(weibo_filter('?wid r:repost ?wid2 . ?wid2 wa:repostsnum ?x ' + fil, limits))
    wid_c = set(weibo_filter('?cid r:cto ?wid ' + fil, limits))
    wid_l = set(weibo_filter('?wid r:likedby u:' + myuid + ' ' + fil, limits))
    weibos = []
    for wid, uid, username, photo, d, text, repostsnum, commentsnum, attitudesnum, topic in rs:
        userID = int(uid)
        if topic != '':
            topic = '#' + topic + '#' + ' '
        username, text, topic = handle_bad_r([username, text, topic])
        rlist = []
        if wid in wid_r:
            rlist = repost_list(wid)
            if len(rlist) > 0:
                rlist = [(userID, username, topic, text)] + rlist
                userID, username, topic, text = rlist[-1]
                rlist = rlist[:-1]
        rshow = ''
        for rr in rlist:
            rshow += rr[1] + '：' + rr[2] + rr[3] + ' // '
        replies = []
        if wid in wid_c:
            replies = [genReply(c, myuid) for c in weibo_reply(wid)]
        # (self, userID, postID, username, text, time, repostsum, commentsum, attitudesum, topic, forwardlist, forwardshow, img_idx, replies)
        # weibo2 = Weibo(2, 2, 'test3', '今天天气真差', '2020年1月1日13:47', 5, 6, 7, '#天气#', [], '', '14', [
        #         Reply(13, 4, 'test4', 'bad', '2020年1月1日13:48', False, '7'),
        #         Reply(14, 5, 'test5', 'not bad', '2020年1月1日13:49', True, '8'),
        #         ])
        wb = Weibo(userID, int(wid), username, text, d, int(repostsnum), int(commentsnum), int(attitudesnum), topic, rlist, rshow, photo, replies)
        wb.myself = (myuid == uid)
        wb.praised = (wid in wid_l)
        weibos.append(wb)
    return weibos

def latest_weibos(myuid):
    myuid = str(myuid)
    return genWeibosFilter('. { { ?wid r:by ?uid . u:%s r:follow ?uid } union { ?wid r:by u:%s } }' % (myuid, myuid), myuid, 'limit 100')

def all_weibos(myuid):
    return genWeibosFilter('', myuid, 'limit 100')

def user_weibos(uid, myuid):
    return genWeibosFilter('. ?wid r:by u:%s' % (uid), myuid, '')

def genTopicText(text):
    if len(text) == 0:
        return '', ''
    topic = ''
    if text[0] == '#':
        pos = text.find('#', 1)
        if pos > 0:
            topic = text[1:pos]
            text = text[pos+1:]
    while text.startswith(' '):
        text = text[1:]
    return topic, text

