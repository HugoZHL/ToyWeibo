
# sudo bin/gbuild toyweibo ../ToyWeibo/sql2rdf/small.nt
# sudo bin/ghttp 9000 toyweibo &
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

def run_sparql(l):
    ret = gc.query(database, 'json', prefix_string + l)
    if not l.startswith('select'):
        gc.checkpoint(database)
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
    return [user_query_value(uid, k) for k in keys]

def user_insert_strings(uid, kv_dict):
    for k,v in kv_dict.items():
        _ = run_sparql('insert data { u:%s ua:%s \"%s\" }' % (uid, k, v))

def user_insert_ints(uid, kv_dict):
    for k,v in kv_dict.items():
        _ = run_sparql('insert data { u:%s ua:%s \"%d\"^^<http://www.w3.org/2001/XMLSchema#integer> }' % (uid, k, v))

def user_delete_values(uid, keys):
    for k in keys:
        _ = run_sparql('delete { ?uid ?k ?v } where { ?uid ?k ?v filter( ?uid = u:%s && ?k = ua:%s ) } ' % (uid, k))

def user_update_int(uid, k, delta):
    v = int(user_query_value(uid, k)[0])
    v += delta
    user_delete_values(uid, [k])
    user_insert_ints(uid, {k:v})



# weibo queries

def weibo_query_values(wid, keys):
    ans = []
    for k in keys:
        result = query('select ?x where { w:%s wa:%s ?x }' % (wid, k))[0]['x']['value']
        ans.append(result)
    return ans

def weibo_insert_ints(wid, kv_dict):
    for k,v in kv_dict.items():
        _ = run_sparql('insert data { w:%s wa:%s \"%d\"^^<http://www.w3.org/2001/XMLSchema#integer> }' % (wid, k, v))

def weibo_delete_values(wid, keys):
    for k in keys:
        _ = run_sparql('delete { ?wid ?k ?v } where { ?wid ?k ?v filter( ?wid = w:%s && ?k = wa:%s ) } ' % (wid, k))

def weibo_update_int(wid, k, delta):
    v = int(weibo_query_values(wid, [k])[0])
    v += delta
    weibo_delete_values(wid, [k])
    weibo_insert_ints(wid, {k:v})



# user account management

def handle_bad(ls):
    return [l.replace('\\', '\\\\').replace('\"', '\\\"') for l in ls]

def register(email, screen_name, password, location, url, gender):
    email, screen_name, password, location, url, gender = handle_bad([email, screen_name, password, location, url, gender])
    if not is_unique('email', email):
        return (False, 'Email already exists')
    if not is_unique('screen_name', screen_name):
        return (False, 'Screen name already exists')
    uid = query('select ?uid where { u:next r:is ?uid }')[0]['uid']['value']
    next_uid = str(int(uid) + 1)
    _ = run_sparql('delete data { u:next r:is \"%s\" }' % (uid))
    _ = run_sparql('insert data { u:next r:is \"%s\" }' % (next_uid))
    user_insert_strings(uid, {'email':email, 'screen_name':screen_name, 'password':password, 'location':location, 'url':url, 'gender':gender})
    user_insert_ints(uid, {'followersnum':0, 'friendsnum':0, 'statusesnum':0}) # followers, followings, weibos
    user_insert_strings(uid, {'created_at':time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())})
    return (True, uid)

def login(email, password):
    email, password = handle_bad([email, password])
    uids = query('select ?uid where { ?uid ua:email \"%s\" . ?uid ua:password \"%s\" }' % (email, password))
    if len(uids) == 0:
        return (False, 'Wrong email or password')
    else:
        uid = uids[0]['uid']['value'][u_len:]
        return (True, uid)

def update_info0(uid, email, screen_name, location, url, gender):
    email, screen_name, location, url, gender = handle_bad([email, screen_name, location, url, gender])
    cur_email, cur_screen_name = user_query_values(uid, ['email', 'screen_name'])
    if not email == cur_email and not is_unique('email', email):
        return (False, 'Email already exists')
    if not screen_name == cur_screen_name and not is_unique('screen_name', screen_name):
        return (False, 'Screen name already exists')
    user_delete_values(uid, ['email', 'screen_name', 'location', 'url', 'gender'])
    user_insert_strings(uid, {'email':email, 'screen_name':screen_name, 'location':location, 'url':url, 'gender':gender})
    return (True, 'Succeeded')

def change_password(uid, old_pwd, new_pwd):
    old_pwd, new_pwd = handle_bad([old_pwd, new_pwd])
    if old_pwd != user_query_value(uid, 'password')[0]:
        return False
    else:
        user_delete_values(uid, ['password'])
        user_insert_strings(uid, {'password': new_pwd})
        return True

def update_info(uid, email, screen_name, password, location, url, gender):
    email, screen_name, password, location, url, gender = handle_bad([email, screen_name, password, location, url, gender])
    cur_email, cur_screen_name = user_query_values(uid, ['email', 'screen_name'])
    if not email == cur_email and not is_unique('email', email):
        return (False, 'Email already exists')
    if not screen_name == cur_screen_name and not is_unique('screen_name', screen_name):
        return (False, 'Screen name already exists')
    user_delete_values(uid, ['email', 'screen_name', 'password', 'location', 'url', 'gender'])
    user_insert_strings(uid, {'email':email, 'screen_name':screen_name, 'password':password, 'location':location, 'url':url, 'gender':gender})
    return (True, 'Succeeded')


# weibo management

def weibo_exists(wid):
    return len(query('select ?d where { w:%s wa:date ?d }' % (wid))) != 0

def weibo_uid(wid):
    return query('select ?uid where { w:%s r:by ?uid }' % (wid))[0]['uid']['value'][u_len:]

def weibo_info(wid):
    #return [wid, weibo_uid(wid)] + weibo_query_values(wid, ['text', 'date', 'attitudesnum'])
    return wid

def latest_weibo(uid):
    ans = []
    wid_urls = query('select distinct ?wid ?d where { { ?wid r:by ?x . u:%s r:follow ?x . ?wid wa:date ?d } union { ?wid r:by u:%s . ?wid wa:date ?d } } order by desc(?d)' % (uid, uid))
    for url in wid_urls:
        wid = url['wid']['value'][w_len:]
        ans.append(weibo_info(wid))
    return ans

def all_weibo():
    ans = []
    wid_urls = query('select ?wid ?d where { ?wid wa:date ?d } order by desc(?d)')
    for url in wid_urls:
        wid = url['wid']['value'][w_len:]
        ans.append(weibo_info(wid))
    return ans

def user_weibo(uid):
    ans = []
    wid_urls = query('select ?wid ?d where { ?wid r:by u:%s . ?wid wa:date ?d } order by desc(?d)' % (uid))
    for url in wid_urls:
        wid = url['wid']['value'][w_len:]
        ans.append(weibo_info(wid))
    return ans
    
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
    return wid

def repost_weibo(wid1, wid2):
    _ = run_sparql('insert data { w:%s r:repost w:%s }' % (wid1, wid2))
    weibo_update_int(wid2, 'repostsnum', 1)

def repost_list(wid):
    ans = []
    wid1 = wid
    wid2_urls = query('select ?wid where { w:%s r:repost ?wid }' % (wid1))
    while len(wid2_urls) > 0:
        wid2 = wid2_urls[0]['wid']['value'][w_len:]
        if not weibo_exists(wid2):
            break
        # userID, username, topic, text
        uid = weibo_uid(wid2)
        screen_name = '@' + user_query_value(uid, 'screen_name')
        topic = ''
        text = '此微博已删除'
        if weibo_exists(wid2):
            topic, text = weibo_query_values(wid2, ['topic', 'text'])
            if topic != '':
                topic = '#' + topic + '#' + ' '
        ans.append((int(uid), screen_name, topic, text))
        wid1 = wid2
        wid2_urls = query('select ?wid where { w:%s r:repost ?wid }' % (wid1))
    return ans

def delete_weibo(wid):
    uid = weibo_uid(wid)
    user_update_int(uid, 'statusesnum', -1)
    wid2_urls = query('select ?wid where { w:%s r:repost ?wid }' % (wid))
    if len(wid2_urls) > 0:
        wid2 = wid2_urls[0]['wid']['value'][w_len:]
        weibo_update_int(wid2, 'repostsnum', -1)
    _ = run_sparql('delete { ?x ?y ?z } where { ?x ?y ?z filter( ?x = w:%s && ?y = wa:date ) )  }' % (wid))





# user relations

def find_user(screen_name):
    uid_urls = query('select ?uid where { ?uid ua:screen_name \"%s\" }' % (screen_name))
    if len(uid_urls) == 0:
        return (False, 'User not exist')
    else:
        return (True, uid_urls[0]['uid']['value'][u_len:])

def find_users(searching):
    keywords = searching.split(' ')
    filters = ''
    for w in keywords:
        if w != '':
            filters += 'filter regex(?x, \"%s\" ) ' % (w)
    uid_urls = query('select ?uid where { ?uid ua:screen_name ?x %s}' % (filters))
    return [url['uid']['value'][u_len:] for url in uid_urls]

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

def is_following_list(uid1, uid2s):
    return [is_following(uid1, uid2) for uid2 in uid2s]

def routes(uid1, uid2, cnt):
    q = 'select'
    for i in range(cnt):
        q += ' ?x%d' % (i)
    q += ' where { u:%s' % (uid1)
    for i in range(cnt):
        q += ' r:follow ?x%d . ?x%d' % (i, i)
    q += ' r:follow u:%s }' % (uid2)
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

def nhops(uid, n):
    q = 'select ?x%d where { u:%s' % (n-1, uid)
    for i in range(n-1):
        q += ' r:follow ?x%d . ?x%d' % (i, i)
    q += ' r:follow ?x%d }' % (n-1)
    data = query(q)
    return [d['x%d' % (n-1)]['value'][u_len:] for d in data]

def nhops_all(uid, n):
    ans = set()
    for i in range(n):
        ans.update(nhops(uid, i+1))
    return list(ans)



# like

def is_liked_by(wid, uid):
    return len(query('select ?r where { w:%s ?r u:%s filter( ?r = r:likedby ) }' % (wid, uid))) != 0

def like_it(wid, uid):
    _ = run_sparql('insert data { w:%s r:likedby u:%s }' % (wid, uid))
    weibo_update_int(wid, 'attitudesnum', 1)

def cancel_like_it(wid, uid):
    _ = run_sparql('delete data { w:%s r:likedby u:%s }' % (wid, uid))
    weibo_update_int(wid, 'attitudesnum', -1)



# reply

def weibo_reply(wid):
    ans = []
    cid_urls = query('select ?cid ?uid ?text ?t where { ?cid r:cto w:%s . ?cid ca:time ?t . ?cid ca:text ?text . ?cid r:cby ?uid } order by desc(?t)' % (wid))
    for url in cid_urls:
        # replyID, userID, username, text, time, myself
        cid = url['cid']['value'][c_len:]
        uid = url['uid']['value'][u_len:]
        username = user_query_value(uid, 'screen_name')
        text = url['text']['value']
        t = url['t']['value']
        ans.append([cid, uid, username, text, t])
    return ans

def send_reply(wid, uid, text):
    cid = query('select ?cid where { c:next r:is ?cid }')[0]['cid']['value']
    next_cid = str(int(cid) + 1)
    _ = run_sparql('delete data { c:next r:is \"%s\" }' % (cid))
    _ = run_sparql('insert data { c:next r:is \"%s\" }' % (next_cid))
    _ = run_sparql('insert data { c:%s ca:text \"%s\" }' % (cid, text))
    _ = run_sparql('insert data { c:%s r:cby u:%s }' % (cid, uid))
    _ = run_sparql('insert data { c:%s r:cto w:%s }' % (cid, wid))
    _ = run_sparql('insert data { c:%s ca:time \"%s\" }' % (cid, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    weibo_update_int(wid, 'commentsnum', 1)
    return cid

def delete_reply(cid):
    wid = query('select ?wid where { c:%s r:cto ?wid }' % (cid))[0]['wid']['value'][w_len:]
    weibo_update_int(wid, 'commentsnum', -1)
    _ = run_sparql('delete { ?x ?y ?z } where { ?x ?y ?z filter( ?x = c:%s && ?y = ca:time ) )  }' % (cid))




# for test

def bunch_register(n):
    for i in range(n):
        x = str(i+1)
        register(x,x,x,'','','')

def bunch_follow(n):
    for i in range(n-1):
        follow(str(i+1), str(i+2))



# some functions for router

def genUserInfo(uid):
    uid = str(uid)
    r = user_query_values(uid, ['screen_name', 'location', 'gender', 'followersnum', 'friendsnum', 'statusesnum', 'created_at'])
    if r[2] == 'f':
        gender = '女'
    elif r[2] == 'm':
        gender = '男'
    else:
        gender = '性别未知或其他'
    infos = {
        'userID': int(uid),
        'name': r[0],
        'location': r[1],
        'gender': gender,
        'followersum': int(r[3]),
        'friendsum': int(r[4]),
        'statusesum': int(r[5]),
        'created_at': r[6],
    }
    return infos

def genUserInfo2(infos, myuid):
    myuid = str(myuid)
    uid = str(infos['userID'])
    infos['following'] = is_following(myuid, uid)
    infos['ismyself'] = (myuid == uid)
    return infos

def genUserInfoEdit(uid):
    uid = str(uid)
    r = user_query_values(uid, ['screen_name', 'email', 'url', 'location', 'gender'])
    if r[4] == 'f':
        gender = '女'
    elif r[4] == 'm':
        gender = '男'
    else:
        gender = ''
    infos = {
        'name': r[0],
        'email': r[1],
        'url': r[2],
        'location': r[3],
        'gender': gender,
    }
    return infos

def genReply(c, myuid):
    myuid = str(myuid)
    myself = (c[1] == myuid)
    # replyID, userID, username, text, time, myself
    return Reply(int(c[0]), int(c[1]), c[2], c[3], c[4], myself)

def genWeibo(wid, myuid):
    wid = str(wid)
    myuid = str(myuid)
    uid = weibo_uid(wid)
    username = user_query_value(uid, 'screen_name')
    r = weibo_query_values(wid, ['text', 'date', 'repostsnum', 'commentsnum', 'attitudesnum', 'topic'])
    userID = int(uid)
    text = r[0]
    topic = r[5]
    if topic != '':
        topic = '#' + topic + '#' + ' '

    rlist = repost_list(wid)
    if len(rlist) > 0:
        rlist = [(userID, username, topic, text)] + rlist
        userID, username, topic, text = rlist[-1]
        rlist = rlist[:-1]
    rshow = ''
    for rr in rlist:
        rshow += rr[1] + '：' + rr[2] + rr[3] + ' // '
    replies = [genReply(c, myuid) for c in weibo_reply(wid)]

    # (self, userID, postID, username, text, time, repostsum, commentsum, attitudesum, topic, forwardlist, forwardshow, replies)
    # weibo2 = Weibo(2, 4, '@test3', '今天天气真差', '2020年1月1日13:47', 5, 6, 7, '#天气#', [(1, 'test2','#感想#', '不错'),
    # (1, '@test3','#感想#', '不错'), (1, '@test4','#感想#', '不错')], 'test2：#感想# 不错 // @test3：#感想# 不错 // @test4：#感想# 不错 // ', [])
    wb = Weibo(userID, int(wid), username, text, r[1], int(r[2]), int(r[3]), int(r[4]), topic, rlist, rshow, replies)
    wb.myself = (myuid == uid)
    wb.praised = is_liked_by(wid, myuid)
    return wb

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

