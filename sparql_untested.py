
# sudo bin/gbuild small ???/small.nt
# sudo bin/ghttp 9000 small
# bin/shutdown 9000
# gdrop small

import GstoreConnector
import json
import time

prefix = {'u':'http://example.org/user/', 
    'w': 'http://example.org/weibo/',
    'ua': 'http://example.org/user_attr/',
    'wa': 'http://example.org/weibo_attr/',
    'r': 'http://example.org/rel/'}
database = 'small'
u_len = len(prefix['u'])
w_len = len(prefix['w'])
gc = GstoreConnector.GstoreConnector('localhost', 9000, 'root', '123456')
_ = gc.load(database)

def transfer(l):
    ls = l.split(' ')
    for lls in ls:
        if ':' in lls:
            llss = lls.split(':')
            uri = '<' + prefix[llss[0]] + llss[1] + '>'
            l = l.replace(lls, uri)
    return l

def run_sparql(l):
    return gc.query(database, 'json', transfer(l))

def query(l):
    return json.loads(run_sparql(l))['results']['bindings']

def is_unique(key, value):
    data = query('select ?x where { ?x ua:%s \"%s\" }' % (key, value))
    if len(data) == 0:
        return True
    else:
        return False

def user_query_values(uid, keys):
    ans = []
    for k in keys:
        result = query('select ?x where { u:%s ua:%s ?x }' % (uid, k))[0]['x']['value']
        ans.append(result)
    return ans

def user_insert_strings(uid, kv_dict):
    for k,v in kv_dict.items():
        _ = run_sparql('insert data { u:%s ua:%s \"%s\" }' % (uid, k, v))

def user_insert_ints(uid, kv_dict):
    for k,v in kv_dict.items():
        _ = run_sparql('insert data { u:%s ua:%s %d }' % (uid, k, v))

def user_delete_values(uid, keys):
    for k in keys:
        _ = run_sparql('delete { ?uid ?k ?v } where { ?uid ?k ?v filter( ?uid = u:%s ) filter( ?k = ua:%s ) } ' % (uid, k))

def user_update_int(uid, k, delta):
    v = user_query_values(uid, [k])[0]
    v += delta
    user_delete_values(uid, [k])
    user_insert_ints(uid, {k:v})

def weibo_query_values(wid, keys):
    ans = []
    for k in keys:
        result = query('select ?x where { w:%s wa:%s ?x }' % (wid, k))[0]['x']['value']
        ans.append(result)
    return ans

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

def update_info(uid, email, screen_name, location, url, gender):
    email, screen_name, location, url, gender = handle_bad([email, screen_name, location, url, gender])
    if not is_unique('email', email):
        return (False, 'Email already exists')
    if not is_unique('screen_name', screen_name):
        return (False, 'Screen name already exists')
    user_delete_values(uid, ['email', 'screen_name', 'location', 'url', 'gender'])
    user_insert_strings(uid, {'email':email, 'screen_name':screen_name, 'location':location, 'url':url, 'gender':gender})

def change_password(uid, old_pwd, new_pwd):
    new_pwd = handle_bad([new_pwd])[0]
    if old_pwd != user_query_values(uid, ['password'])[0]:
        return False
    else:
        user_delete_values(uid, ['password'])
        user_insert_ints(uid, {'password', new_pwd})

def weibo_info(wid):
    return [wid] + weibo_query_values(wid, ['text']) # TODO what to show?

def latest_weibo(uid):
    ans = []
    wid_urls = query('select ?wid where { ?wid r:by ?x . u:%s r:follow ?x . ?wid wa:date ?d } order by desc(?d)' % (uid))
    for url in wid_urls:
        wid = url[w_len:]
        ans.append(weibo_info(wid))
    return ans

def user_weibo(uid):
    ans = []
    wid_urls = query('select ?wid where { ?wid r:by u:%s . ?wid wa:date ?d } order by desc(?d)' % (uid))
    for url in wid_urls:
        wid = url[w_len:]
        ans.append(weibo_info(wid))
    return ans
    
def send_weibo(uid, text):
    text = handle_bad([text])[0]
    wid = query('select ?wid where { w:next r:is ?wid }')[0]['wid']['value']
    next_wid = str(int(wid) + 1)
    _ = run_sparql('delete data { w:next r:is \"%s\" }' % (wid))
    _ = run_sparql('insert data { w:next r:is \"%s\" }' % (next_wid))
    _ = run_sparql('insert data { w:%s ua:text \"%s\" }' % (wid, text))
    _ = run_sparql('insert data { w:%s r:by u:%s }' % (wid, uid))
    _ = run_sparql('insert data { w:%s ua:commentsnum 0 }' % (wid))
    _ = run_sparql('insert data { w:%s ua:date \"%s\" }' % (wid, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))

def find_user(screen_name):
    uid_urls = query('select ?uid where { ?uid ua:screen_name \"%s\" }' % (screen_name))
    if len(uid_urls) == 0:
        return False
    else:
        return uid_urls[0]['uid']['value'][u_len:]

def followers(uid):
    uid_urls = query('select ?uid where { ?uid r:follow u:%s }' % {uid})
    return [url['uid']['value'][u_len:] for url in uid_urls]

def followings(uid):
    uid_urls = query('select ?uid where { u:%s r:follow ?uid }' % {uid})
    return [url['uid']['value'][u_len:] for url in uid_urls]

def follow(uid1, uid2):
    _ = run_sparql('insert data { u:%s r:follow u:%s }' % (uid1, uid2))

def unfollow(uid1, uid2):
    _ = run_sparql('delete data { u:%s r:follow u:%s }' % (uid1, uid2))

def routes(uid1, uid2, cnt):
    q = 'select'
    for i in range(cnt):
        q += ' ?x%d' % (i)
    q += ' where { u:%s' % (uid1)
    for i in range(cnt-1):
        q += ' r:follow ?x%d . ?x%d' % (i, i+1)
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
    if len(query('select ?r where { u:%s ?r u:%s }' % (uid1, uid2))) != 0:
        ans.append([uid1, uid2])
    for i in range(3):
        ans += routes(uid1, uid2, i+1)
    return ans
