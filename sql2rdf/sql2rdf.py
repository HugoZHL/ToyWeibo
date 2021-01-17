
import time
import random

user_attrs = ['uid', 'screen_name', 'name', 'province', 'city', 'location', 'url', 'gender', 'followersnum', 'friendsnum', 'statusesnum', 'favouritesnum', 'created_at']
weibo_attrs = ['mid', 'date', 'text', 'source', 'repostsnum', 'commentsnum', 'attitudesnum', 'uid', 'topic']

f = open('small.sql', 'r')
o = open('small.nt', 'w')

o.writelines(['@prefix u:   <http://example.org/user/> .\n'])
o.writelines(['@prefix w:   <http://example.org/weibo/> .\n'])
o.writelines(['@prefix c:   <http://example.org/comment/> .\n'])
o.writelines(['@prefix ua:  <http://example.org/user_attr/> .\n'])
o.writelines(['@prefix wa:  <http://example.org/weibo_attr/> .\n'])
o.writelines(['@prefix ca:  <http://example.org/comment_attr/> .\n'])
o.writelines(['@prefix r:   <http://example.org/rel/> .\n\n'])

def parse_string(l, cnt, long_id):
    pos = l.find('(')
    attrs = l.strip()[pos+1 : -2].split(', ')
    while len(attrs) > cnt:
        attrs[long_id] += ', ' + attrs[long_id+1]
        _ = attrs.pop(long_id+1)
    result = []
    for attr in attrs:
        res = attr.replace('\"', '\\\"')
        if res[0] == '\'':
            result.append('\"' + res[1:-1] + '\"')
        else:
            result.append(res)
    return result

maxuid = 0
maxwid = 0

for l in f.readlines():
    if 'INSERT INTO `user`' in l:
        attrs = parse_string(l, len(user_attrs), 0)
        uid = attrs[0][1:-1]
        maxuid = max(maxuid, int(uid))
        for i in range(len(attrs)-1):
            o.writelines([ 'u:' + uid + ' ua:' + user_attrs[i+1] + ' ' + attrs[i+1] + ' .\n' ])
        o.writelines([ 'u:' + uid + ' ua:password \"123\" .\n' ])
        o.writelines([ 'u:' + uid + ' ua:email \"' + uid + '@t\" .\n' ])
        o.writelines([ 'u:' + uid + ' ua:photo \"' + str(random.randint(0, 25)) + '\" .\n' ])

    if 'INSERT INTO `userrelation`' in l:
        pos1 = l.find('(')
        pos2 = l.find(',')
        pos3 = l.find(')')
        uid1 = l[pos1+2 : pos2-1]
        uid2 = l[pos2+3 : pos3-1]
        o.writelines([ 'u:' + uid1 + ' r:follow u:' + uid2 + ' .\n' ])
    if 'INSERT INTO `weibo`' in l:
        attrs = parse_string(l, len(weibo_attrs), 2)
        wid = attrs[0][1:-1]
        uid = attrs[-2][1:-1]
        maxwid = max(maxwid, int(wid))
        for i in range(len(attrs)-3):
            o.writelines([ 'w:' + wid + ' wa:' + weibo_attrs[i+1] + ' ' + attrs[i+1] + ' .\n' ])
        o.writelines([ 'w:' + wid + ' wa:' + weibo_attrs[-1] + ' ' + attrs[-1] + ' .\n' ])
        o.writelines([ 'w:' + wid + ' r:by u:' + uid + ' .\n' ])
    if 'INSERT INTO `weiborelation`' in l:
        pos1 = l.find('(')
        pos2 = l.find(',')
        pos3 = l.find(')')
        wid1 = l[pos1+2 : pos2-1]
        wid2 = l[pos2+3 : pos3-1]
        o.writelines([ 'w:' + wid1 + ' r:repost w:' + wid2 + ' .\n' ])

f.close()
o.writelines([ '\nw:' + str(maxwid) + ' r:likedby u:' + str(maxuid) + ' .\n' ])

o.writelines([ 'c:1 ca:text \"nice\" .\n' ])
o.writelines([ 'c:1 ca:time \"' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\" .\n' ])
o.writelines([ 'c:1 r:cby u:' + str(maxuid) + ' .\n' ])
o.writelines([ 'c:1 r:cto w:' + str(maxwid) + ' .\n' ])

o.writelines([ 'u:next r:is \"' + str(maxuid+1) + '\" .\n' ])
o.writelines([ 'w:next r:is \"' + str(maxwid+1) + '\" .\n' ])
o.writelines([ 'c:next r:is \"2\" .\n' ])
o.close()
